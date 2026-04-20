from django.urls import path
from core.views.centrales_view import (
  CentraleListView,
  CentraleDetailView,
  CentraleCreateView,
  CentraleUpdateView,
  CentralePartialUpdateView,
  CentraleDeleteView,
)

from core.views.poissons_view import (
  PoissonListView,
  PoissonDetailView,
  PoissonCreateView,
  PoissonUpdateView,
  PoissonPartialUpdateView,
  PoissonDeleteView,
)

from core.views.non_poissons_view import (
  NonPoissonListView,
  NonPoissonDetailView,
  NonPoissonCreateView,
  NonPoissonUpdateView,
  NonPoissonPartialUpdateView,
  NonPoissonDeleteView,
)

from core.views.echantillonnage_view import (
  EchantillonnageListView,
  EchantillonnageDetailView,
  EchantillonnageCreateView,
  EchantillonnageUpdateView,
  EchantillonnagePartialUpdateView,
  EchantillonnageDeleteView,
)

from core.views.inventaire_milieu_view import (
  InventaireMilieuListView,
  InventaireMilieuDetailView,
  InventaireMilieuCreateView,
  InventaireMilieuUpdateView,
  InventaireMilieuPartialUpdateView,
  InventaireMilieuDeleteView,
)

from core.views.dynamic_query_view import (
    QueryBuilderMetadataView,
    QueryBuilderExecuteView,
)

from core.views.app_user_view import (
    AppUserListView,
    AppUserDetailView,
    AppUserCreateView,
    AppUserPartialUpdateView,
    AppUserDeleteView,
)

from core.views.iri_poisson_view import IriPoissonView

urlpatterns = [
  path("centrales/", CentraleListView.as_view(), name="centrales-list"),
  path("centrales/<int:centrale_id>/", CentraleDetailView.as_view(), name="centrales-detail"),

  path("centrales/create/", CentraleCreateView.as_view(), name="centrales-create"),
  path("centrales/<int:centrale_id>/update/", CentraleUpdateView.as_view(), name="centrales-update"),
  path("centrales/<int:centrale_id>/partial/", CentralePartialUpdateView.as_view(), name="centrales-partial-update"),
  path("centrales/<int:centrale_id>/delete/", CentraleDeleteView.as_view(), name="centrales-delete"),
  path("poissons/", PoissonListView.as_view(), name="poissons-list"),
  path("poissons/<int:poisson_id>/", PoissonDetailView.as_view(), name="poissons-detail"),

  path("poissons/create/", PoissonCreateView.as_view(), name="poissons-create"),
  path("poissons/<int:poisson_id>/update/", PoissonUpdateView.as_view(), name="poissons-update"),
  path("poissons/<int:poisson_id>/partial/", PoissonPartialUpdateView.as_view(), name="poissons-partial-update"),
  path("poissons/<int:poisson_id>/delete/", PoissonDeleteView.as_view(), name="poissons-delete"),

  path("non-poissons/", NonPoissonListView.as_view(), name="non-poissons-list"),
  path("non-poissons/<int:non_poisson_id>/", NonPoissonDetailView.as_view(), name="non-poissons-detail"),

  path("non-poissons/create/", NonPoissonCreateView.as_view(), name="non-poissons-create"),
  path("non-poissons/<int:non_poisson_id>/update/", NonPoissonUpdateView.as_view(), name="non-poissons-update"),
  path("non-poissons/<int:non_poisson_id>/partial/", NonPoissonPartialUpdateView.as_view(), name="non-poissons-partial-update"),
  path("non-poissons/<int:non_poisson_id>/delete/", NonPoissonDeleteView.as_view(), name="non-poissons-delete"),

  path("echantillonnages/", EchantillonnageListView.as_view(), name="echantillonnages-list"),
  path("echantillonnages/<int:echantillonnage_id>/", EchantillonnageDetailView.as_view(), name="echantillonnages-detail"),

  path("echantillonnages/create/", EchantillonnageCreateView.as_view(), name="echantillonnages-create"),
  path("echantillonnages/<int:echantillonnage_id>/update/", EchantillonnageUpdateView.as_view(), name="echantillonnages-update"),
  path("echantillonnages/<int:echantillonnage_id>/partial/", EchantillonnagePartialUpdateView.as_view(), name="echantillonnages-partial-update"),
  path("echantillonnages/<int:echantillonnage_id>/delete/", EchantillonnageDeleteView.as_view(), name="echantillonnages-delete"),

  path("inventaires-milieu/", InventaireMilieuListView.as_view(), name="inventaires-milieu-list"),
  path("inventaires-milieu/<int:inventaire_id>/", InventaireMilieuDetailView.as_view(), name="inventaires-milieu-detail"),

  path("inventaires-milieu/create/", InventaireMilieuCreateView.as_view(), name="inventaires-milieu-create"),
  path("inventaires-milieu/<int:inventaire_id>/update/", InventaireMilieuUpdateView.as_view(), name="inventaires-milieu-update"),
  path("inventaires-milieu/<int:inventaire_id>/partial/", InventaireMilieuPartialUpdateView.as_view(), name="inventaires-milieu-partial-update"),
  path("inventaires-milieu/<int:inventaire_id>/delete/", InventaireMilieuDeleteView.as_view(), name="inventaires-milieu-delete"),

  path("query-builder/metadata/", QueryBuilderMetadataView.as_view(), name="query-builder-metadata"),
  path("query-builder/execute/", QueryBuilderExecuteView.as_view(), name="query-builder-execute"),
  path("users/", AppUserListView.as_view(), name="app-users-list"),
  path("users/<int:app_user_id>/", AppUserDetailView.as_view(), name="app-users-detail"),

  path("users/create/", AppUserCreateView.as_view(), name="app-users-create"),
  path("users/<int:app_user_id>/partial/", AppUserPartialUpdateView.as_view(), name="app-users-partial-update"),
  path("users/<int:app_user_id>/delete/", AppUserDeleteView.as_view(), name="app-users-delete"),
  path("poissons/iri/", IriPoissonView.as_view(), name="iri-poissons"),
]
