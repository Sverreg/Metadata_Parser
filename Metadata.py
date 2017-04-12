from ij import IJ
from loci.formats import ImageReader
from loci.formats import MetadataTools

def Metadata(File):
	""" Iterates through .lif XML/OME metadata, returns selected values eg. timepoints, channels, series count, laser power.. """

	# Calls ImageReader and MetadataTools
	reader = ImageReader()
	omeMeta = MetadataTools.createOMEXMLMetadata()
	reader.setMetadataStore(omeMeta)
	reader.setId(File)

	# Gets number of image series, channel number
	seriesCount = reader.getSeriesCount()
	channels = reader.getSizeC()
	LP = reader.getLightSourceSettingsAttenuation()
	reader.close()

	# Number of images
	imageCount = omeMeta.getImageCount()

	# Laser power 458
	LP = omeMeta.getChannelLightSourceSettingsAttenuation(0,0)
	LP = 1 - LP.getNumberValue()
	
	timelist = []

	# Timepoints
	for timepoint in range (seriesCount):
		time = [omeMeta.getImageAcquisitionDate(timepoint)]
		timelist.append(time)

	# Dirty hours/minutes timepointhack
	time = [str(s1[0])[11:] for s1 in timelist]
	
	IJ.log("Total # of image series (from BF reader): " + str(seriesCount))
	IJ.log("Total # of image series (from OME metadata): " + str(imageCount))
	IJ.log("Total # of channels (from OME metadata): " + str(channels))
	IJ.log("LP (from OME metadata): " + str(LP))
	
	return channels, seriesCount, time, LP