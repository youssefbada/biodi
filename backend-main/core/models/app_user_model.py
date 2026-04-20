from django.db import models


class AppUserRole(models.TextChoices):
  ADMIN = "ADMIN", "Admin"
  READ_ONLY = "READ_ONLY", "Read only"


class AppUser(models.Model):
  """
  Utilisateur applicatif Biodiv.
  Authentification via OIDC.
  Cette table sert à autoriser/refuser l'accès et porter le rôle applicatif.
  """

  id = models.AutoField(primary_key=True)

  nni = models.CharField(
    max_length=255,
    unique=True,
    db_index=True,
    blank=True,
    null=True,
    help_text="Identifiant unique renvoyé par le provider OIDC (claim 'sub').",
  )

  first_name = models.CharField(max_length=150, blank=True)
  last_name = models.CharField(max_length=150, blank=True)

  email = models.EmailField(unique=True, db_index=True)

  role = models.CharField(
    max_length=20,
    choices=AppUserRole.choices,
    default=AppUserRole.READ_ONLY,
    db_index=True,
  )

  is_active = models.BooleanField(default=True, db_index=True)

  last_login_at = models.DateTimeField(null=True, blank=True)

  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    db_table = "app_users"
    verbose_name = "Application user"
    verbose_name_plural = "Application users"
    ordering = ["email"]
    indexes = [
      models.Index(fields=["email"], name="idx_app_user_email"),
      models.Index(fields=["role"], name="idx_app_user_role"),
      models.Index(fields=["is_active"], name="idx_app_user_active"),
    ]

  def __str__(self) -> str:
    full_name = f"{self.first_name or ''} {self.last_name or ''}".strip()
    if full_name:
      return f"{full_name} <{self.email}>"
    return self.email