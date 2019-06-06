#
	#
		#
			# ALTERNATIVE MOVIE POSTERS :: AGENT FOR PLEX
				# BY KITSUNE.WORK — 2018-2019
			# VERSION 0.94
		#
	#
#

# FUTURE ATTEMPT AT DETECTING AND REMOVING BORDERS
#import PIL

PLUGIN_VERSION = '0.94'

####################################################################################################

def Start():
	HTTP.CacheTime = CACHE_1WEEK
	HTTP.Headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/604.3.5 (KHTML, like Gecko) Version/11.0.1 Safari/604.3.5'
	# -----------------------------------------------------------------------------|
	# PING THE CREATOR OF THIS AGENT TO RECORD USAGE 							   |
	# NOTHING CREEPY, JUST WANT TO KNOW HOW MUCH TIME TO INVEST 				   |
	# BASED ON HOW MANY PEOPLE USE MY WORK 										   |
	# I HAVE TO USE SOME KIND OF UNIQUE IDENTIFIER TO MAKE SURE STATS ARE ACCURATE |
	# -----------------------------------------------------------------------------|
	ID 	= HTTP.Request('https://plex.tv/pms/:/ip').content
	RNG	= HTTP.Request('http://projects.kitsune.work/aTV/AMP/ping.php?ID='+str(ID)).content

####################################################################################################

# :: MOVIES AGENT # com_plexapp_agents_themoviedb
class AltMoviePostersAgent(object):
	languages = [Locale.Language.NoLanguage]
	primary_provider = False

	def __init__(self, *args, **kwargs):
		super(AltMoviePostersAgent, self).__init__(*args, **kwargs)
		self.agent_type = "MOVIES" if isinstance(self, Agent.Movies) else "SERIES"
		self.name = "AltMoviePosters (%s, %s)" % (self.agent_type_verbose, PLUGIN_VERSION)

	def search(self, results, media, lang):
		Log(':: ALTMOVIEPOSTERS (%s) STARTED ::' % self.agent_type)
		if media.primary_metadata is not None:
			results.Append(MetadataSearchResult(
				id = media.primary_metadata.id,
				score = 100
			))

	def update(self, metadata, media, lang):
		#processTitle(str(media.title))
		# PROCESS TITLE
		title 			= str(media.title)
		i 				= 1
		valid_names 	= list()
		foundPosters 	= []
		lastPage		= False

		# CLEAN UP ACCENTS FROM TITLE FOR BETTER SEARCH RESULTS 
		title = title.replace('à', 'a')
		title = title.replace('á', 'a')
		title = title.replace('â', 'a')
		title = title.replace('ä', 'a')
		title = title.replace('æ', 'ae')
		title = title.replace('ã', 'a')
		title = title.replace('å', 'a')
		title = title.replace('ā', 'a')
		title = title.replace('è', 'e')
		title = title.replace('é', 'e')
		title = title.replace('ê', 'e')
		title = title.replace('ë', 'e')
		title = title.replace('ē', 'e')
		title = title.replace('ė', 'e')
		title = title.replace('ę', 'e')
		title = title.replace('î', 'i')
		title = title.replace('ï', 'i')
		title = title.replace('í', 'i')
		title = title.replace('ī', 'i')
		title = title.replace('į', 'i')
		title = title.replace('ì', 'i')
		title = title.replace('ô', 'o')
		title = title.replace('ö', 'o')
		title = title.replace('ò', 'o')
		title = title.replace('ó', 'o')
		title = title.replace('œ', 'o')
		title = title.replace('ø', 'o')
		title = title.replace('ō', 'o')
		title = title.replace('õ', 'o')
		title = title.replace('û', 'u')
		title = title.replace('ü', 'u')
		title = title.replace('ù', 'u')
		title = title.replace('ú', 'u')
		title = title.replace('ū', 'u')
		title = title.replace('ý', 'y')
		title = title.replace('ÿ', 'y')
		Log(':: SEARCHING POSTERS FOR :: %s' % title)
		# -----------------------------------------------------

		# FIND EACH IMG'S SRC
		if title is not None:
			# GET ALL PAGES TILL NO MORE POSTERS ARE FOUND ON THE PAGE
			while not lastPage:
				SEARCHURL = 'http://www.alternativemovieposters.com/page/'+str(i)+'/?s=%s'
				try:
					html = HTML.ElementFromURL(
						SEARCHURL % (String.Quote(title, usePlus=True)),
						errors='ignore'
					)
					i += 1

					# IF NO MORE POSTERS FOUND
					if not html.xpath('//*[@class="fusion-image-wrapper"]'):
						lastPage = True
					else:
						# ELSE SAVE EACH FOUND POSTER FOR PROCESSING WHEN PAGES ARE DONE
						foundPosters += html.xpath('//*[@class="fusion-image-wrapper"]/a/img/@src')
				except:
					# ON ANY KIND OF ERROR ASSUME THE PAGE WAS NOT FOUND
					lastPage = True

			# DONE CHECKING AS MANY PAGES AS POSSIBLE
			i = i-1 # MINUS ONE FOR THE LAST PAGE THAT TOLD THE SCRIPT THERE WERE NO MORE POSTERS
			if i is 1:
				Log(':: PROCESSED :: %s :: PAGE ::' % i)
			else:
				Log(':: PROCESSED :: %s :: PAGES ::' % i)

			# RESET INDEX VAR FOR FOUNDPOSTER ARRAY USE
			i = 0

			# IF NO POSTER ARE FOUND
			if not foundPosters:
				Log(':: NO POSTERS FOUND FOR :: %s' % title)

			# GET URL FOR EACH POSTER
			for poster in foundPosters:
				if poster not in metadata.posters:
					Log.Debug(':: FOUND POSTER :: %s' % poster)
					metadata.posters[poster] = Proxy.Preview(HTTP.Request(poster), sort_order=i)

####################################################################################################

# REGISTER AGENTS
class AltMoviePostersMovies(AltMoviePostersAgent, Agent.Movies):
	agent_type_verbose = "Movies"

class AltMoviePostersTvShows(AltMoviePostersAgent, Agent.TV_Shows):
	agent_type_verbose = "TV"
