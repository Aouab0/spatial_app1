import ee

class SpatialProcessor:
    def __init__(self):
        """initialise la connexion à google earth engine"""
        ee.Initialize(project="training-462609")

    def get_satellite_image(self, lat, lon):
        """recupere la dernière image sentinel pour un point"""
        point = ee.Geometry.Point([lon, lat])

        image = (
            ee.ImageCollection('COPERNICUS/S2_SR')
            .filterBounds(point)
            .sort('CLOUDY_PIXEL_PERCENTAGE')
            .first()
        )
        return image
