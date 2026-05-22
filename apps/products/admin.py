from django import forms
from django.contrib import admin, messages
from django.utils.html import format_html
from django.urls import path
from django.shortcuts import redirect, get_object_or_404
from django.template.response import TemplateResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from .models import WigProduct, WigImage, InchPricing, Review, Category,HeroImage   
from .widgets import MultipleFileField


# ─── Form for traditional bulk upload (kept for fallback) ───────────────────

class BulkImageUploadForm(forms.Form):
    images = MultipleFileField(
        label="Images",
        help_text="Hold Ctrl/Cmd to select multiple images",
    )
    set_first_as_primary = forms.BooleanField(
        required=False,
        initial=True,
        label="Set first uploaded image as primary?",
    )


class WigImageInline(admin.TabularInline):
    model   = WigImage
    extra   = 1
    fields  = ("image_preview", "image", "alt_text", "is_primary", "order")
    readonly_fields = ("image_preview",)

    def image_preview(self, obj):
        if obj.pk and obj.image:
            return format_html(
                '<img src="{}" width="70" height="90" '
                'style="object-fit:cover;border-radius:4px;border:1px solid #e0d8d0"/>',
                obj.image.url,
            )
        return "—"
    image_preview.short_description = "Preview"


class InchPricingInline(admin.TabularInline):
    model   = InchPricing
    extra   = 4
    fields  = ("inches", "price", "stock_quantity", "is_available")


@admin.register(WigProduct)
class WigProductAdmin(admin.ModelAdmin):
    list_display    = (
        "product_thumbnail", "name", "category", "hair_type",
        "lace_type", "density", "is_featured", "is_trending", "is_active", "created_at",
    )
    list_filter     = ("category", "hair_type", "lace_type", "is_featured", "is_trending", "is_active")
    search_fields   = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}
    list_editable   = ("is_featured", "is_trending", "is_active")
    inlines         = [WigImageInline, InchPricingInline]
    save_on_top     = True

    # ─── Custom URLs ──────────────────────────────────────────────────────────
    def get_urls(self):
        urls = super().get_urls()
        custom = [
            path(
                "<uuid:product_id>/bulk-upload/",
                self.admin_site.admin_view(self.bulk_upload_view),
                name="products_wigproduct_bulk_upload",
            ),
            path(
                "<uuid:product_id>/api-upload/",
                self.admin_site.admin_view(self.api_upload_view),
                name="products_wigproduct_api_upload",
            ),
        ]
        return custom + urls

    # ─── Traditional bulk upload view (form-based) ─────────────────────────────
    def bulk_upload_view(self, request, product_id):
        product = get_object_or_404(WigProduct, id=product_id)

        if request.method == "POST":
            form = BulkImageUploadForm(request.POST, request.FILES)
            if form.is_valid():
                files = request.FILES.getlist("images")
                set_primary = form.cleaned_data.get("set_first_as_primary", True)

                if not files:
                    messages.error(request, "No images were selected.")
                else:
                    created = self._process_uploaded_files(product, files, set_primary)
                    messages.success(
                        request,
                        f"{created} image{'s' if created != 1 else ''} uploaded successfully.",
                    )
                    return redirect(f"../../{product_id}/change/")
            else:
                messages.error(request, "Please correct the errors below.")
        else:
            form = BulkImageUploadForm()

        context = {
            **self.admin_site.each_context(request),
            "form": form,
            "product": product,
            "title": f"Bulk Upload Images — {product.name}",
            "opts": self.model._meta,
        }
        return TemplateResponse(request, "admin/bulk_image_upload.html", context)

    # ─── API upload view (fetch/XHR endpoint) ──────────────────────────────────
    @method_decorator(csrf_exempt)
    def api_upload_view(self, request, product_id):
        """Handle AJAX/fetch multi-file upload from admin modal."""
        if request.method != "POST":
            return JsonResponse({"error": "POST only"}, status=405)

        product = get_object_or_404(WigProduct, id=product_id)
        files = request.FILES.getlist("images")
        set_primary = request.POST.get("set_first_as_primary") == "true"

        if not files:
            return JsonResponse({"error": "No images provided"}, status=400)

        try:
            created = self._process_uploaded_files(product, files, set_primary)
            return JsonResponse({
                "success": True,
                "created": created,
                "message": f"{created} image{'s' if created != 1 else ''} uploaded",
            })
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    # ─── Shared file processing logic ────────────────────────────────────────────
    def _process_uploaded_files(self, product, files, set_primary):
        """Create WigImage records from uploaded files."""
        created = 0
        existing_count = WigImage.objects.filter(product=product).count()

        for idx, f in enumerate(files):
            is_primary = (idx == 0 and set_primary and existing_count == 0)
            WigImage.objects.create(
                product=product,
                image=f,
                alt_text=f.name.rsplit(".", 1)[0].replace("-", " ").replace("_", " ").title(),
                is_primary=is_primary,
                order=existing_count + idx,
            )
            created += 1

        return created

    def product_thumbnail(self, obj):
        img = obj.primary_image
        if img:
            return format_html(
                '<img src="{}" width="60" height="75" '
                'style="object-fit:cover;border-radius:4px;border:1px solid #e0d8d0"/>',
                img.image.url,
            )
        return "—"
    product_thumbnail.short_description = "Preview"

    # ─── Inject upload modal + button into change form ─────────────────────────
    def change_view(self, request, object_id, form_url="", extra_context=None):
        extra_context = extra_context or {}
        extra_context["bulk_upload_url"] = f"../{object_id}/bulk-upload/"
        extra_context["api_upload_url"] = f"../{object_id}/api-upload/"
        extra_context["show_upload_modal"] = True
        return super().change_view(request, object_id, form_url, extra_context)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display        = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(HeroImage)
class HeroImageAdmin(admin.ModelAdmin):
    list_display  = ('slot', 'image_preview', 'is_active', 'updated_at')
    list_editable = ('is_active',)

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="80" height="80" style="object-fit:cover;border-radius:4px"/>',
                obj.image.url,
            )
        return '—'
    image_preview.short_description = 'Preview'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display  = ("reviewer_name", "product", "rating", "is_approved", "created_at")
    list_filter   = ("is_approved", "rating", "product")
    list_editable = ("is_approved",)
    search_fields = ("reviewer_name", "message", "product__name")
    actions       = ["approve_reviews", "reject_reviews"]

    def approve_reviews(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f"{updated} review(s) approved.")
    approve_reviews.short_description = "Approve selected reviews"

    def reject_reviews(self, request, queryset):
        updated = queryset.update(is_approved=False)
        self.message_user(request, f"{updated} review(s) rejected.")
    reject_reviews.short_description = "Reject selected reviews"