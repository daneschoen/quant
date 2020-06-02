from apps.app_util import mongodb_import


# Maxmind
# -------
# mongodb_import.import_geo_cnty(bl_drop_col_geo_cnty=True)


# Geonames
# --------
mongodb_import.import_city(bl_drop_col=True)
#mongodb_import.import_cnty(bl_drop_col=True)

#mongodb_import.update_city_timezone()
#mongodb_import.update_city_cnty()


