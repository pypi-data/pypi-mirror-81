import re
from . import errors

pathParamPattern = re.compile(r'\{([^\}]+)\}')
basePath = 'https://www.bungie.net/Platform'

class API:
    def __init__(self, apiKey, session, appID='', appName='', version='', url='', contactEmail=''):
        self.headers = {'X-API-KEY': apiKey}
        if (appID + appName + version + url + contactEmail): # If any of the info for user agents are provided we will fill it in, as described here https://github.com/Bungie-net/api#are-there-any-restrictions-on-the-api
            self.headers['User-Agent'] = f'{appName}/{version} AppId/{appID} (+{url};{contactEmail})'
        
        self.session = session
    
    async def _get(self, url, authorization=None, **params):
        for k in params:
            if params[k] is None:
                del params[k]
        
        headers = dict(self.headers)
        if authorization is not None:
            headers['Authorization'] = authorization
        
        async with self.session.get(url, headers=headers, params=params) as response:
            try:
                data = await response.json()
            except:
                raise ValueError('Destiny API returned a non JSON response')
        
        if data['ThrottleSeconds'] > 0:
            await asyncio.sleep(data['ThrottleSeconds'])
            return await self._get(url, **params)
        
        if data['ErrorCode'] != 1:
            raise errors.DestinyAPIError(data['ErrorCode'])
        
        return data['Response']
    
    async def _post(self, url, data, authorization=None, **params):
        for k in params:
            if params[k] is None:
                del params[k]
        
        headers = dict(self.headers)
        if authorization is not None:
            headers['Authorization'] = authorization

        async with self.session.post(url, headers=headers, data=data, params=params) as response:
            try:
                data = await response.json()
            except:
                raise ValueError('Destiny API returned a non JSON response')
            
        if data['ThrottleSeconds'] > 0:
            await asyncio.sleep(data['ThrottleSeconds'])
            return await self._post(url, data, **params)
        
        if data['ErrorCode'] != 1:
            raise errors.DestinyAPIError(data['ErrorCode'])
        
        return data['Response']

    async def getApplicationApiUsage(self, applicationId, authorization, start=None, end=None):
        return await self._get(basePath + f'/App/ApiUsage/{applicationId}/', authorization=authorization, start=start, end=end)
    
    async def getBungieApplications(self):
        return await self._get(basePath + '/App/FirstParty/')
    
    async def getBungieNetUserById(self, id):
        return await self._get(basePath + f'/User/GetBungieNetUserById/{id}/')
    
    async def searchUsers(self, q):
        return await self._get(basePath + '/User/SearchUsers/', q=q)
    
    async def getAvailableThemes(self):
        return await self._get(basePath + '/User/GetAvailableThemes/')
    
    async def getMembershipDataById(self, membershipId, membershipType):
        return await self._get(basePath + f'/User/GetMembershipsById/{membershipId}/{membershipType}/')
    
    async def getMembershipDataForCurrentUser(self, authorization):
        return await self._get(basePath + '/User/GetMembershipsForCurrentUser/', authorization=authorization)
    
    async def getMembershipFromHardLinkedCredential(self, credential):
        return await self._get(basePath + f'/User/GetMembershipFromHardLinkedCredential/SteamId/{credential}/')
    
    async def getContentType(self, type):
        return await self._get(basePath + f'/Content/GetContentType/{type}/')
    
    async def getContentById(self, id, locale):
        return await self._get(basePath + f'/Content/GetContentById/{id}/{locale}/')
    
    async def getContentByTagAndType(self, tag, type, locale):
        return await self._get(basePath + f'/Content/GetContentByTagAndType/{tag}/{type}/{locale}/')
    
    async def searchContentWithText(self, locale):
        return await self._get(basePath + f'/Content/Search/{locale}/')
    
    async def searchContentByTagAndType(self, credential):
        return await self._get(basePath + f'/User/GetMembershipFromHardLinkedCredential/SteamId/{credential}/')
    
    async def searchHelpArticles(self, searchtext, size):
        return await self._get(basePath + f'/Content/SearchHelpArticles/{searchtext}/{size}/')
    
    async def getTopicsPaged(self, page, pageSize, group, sort, quickDate, categoryFilter, locales='en', tagstring=None):
        return await self._get(basePath + f'/Forum/GetTopicsPaged/{page}/{pageSize}/{group}/{sort}/{quickDate}/{categoryFilter}/', locales=locales, tagstring=tagstring)
    
    async def getCoreTopicsPaged(self, page, sort, quickDate, categoryFilter, locales='en'):
        return await self._get(basePath + f'/Forum/GetCoreTopicsPaged/{page}/{sort}/{quickDate}/{categoryFilter}/', locales=locales)
    
    async def getPostsThreadedPaged(self, parentPostId, page, pageSize, replySize, getParentPost, rootThreadMode, sortMode, showbanned=None):
        return await self._get(basePath + f'/Forum/GetPostsThreadedPaged/{parentPostId}/{page}/{pageSize}/{replySize}/{getParentPost}/{rootThreadMode}/{sortMode}/', showbanned=showbanned)
    
    async def getPostsThreadedPagedFromChild(self, childPostId, page, pageSize, replySize, rootThreadMode, sortMode, showbanned=None):
        return await self._get(basePath + f'/Forum/GetPostsThreadedPagedFromChild/{childPostId}/{page}/{pageSize}/{replySize}/{rootThreadMode}/{sortMode}/', showbanned=showbanned)
    
    async def getPostAndParent(self, childPostId, showbanned=None):
        return await self._get(basePath + f'/Forum/GetPostAndParent/{childPostId}/', showbanned=showbanned)
    
    async def getPostAndParentAwaitingApproval(self, childPostId, showbanned=None):
        return await self._get(basePath + f'/Forum/GetPostAndParentAwaitingApproval/{childPostId}/', showbanned=showbanned)
    
    async def getTopicForContent(self, contentId):
        return await self._get(basePath + f'/Forum/GetTopicForContent/{contentId}/')
    
    async def getForumTagSuggestions(self, partialtag):
        return await self._get(basePath + '/Forum/GetForumTagSuggestions/', partialtag=partialtag)
    
    async def getPoll(self, topicId):
        return await self._get(basePath + f'/Forum/Poll/{topicId}/')

    async def getRecruitmentThreadSummaries(self, data):
        return await self._post(basePath + '/Forum/Recruit/Summaries/', data)
    
    async def getAvailableAvatars(self):
        return await self._get(basePath + '/GroupV2/GetAvailableAvatars/')
    
    async def getAvailableThemes(self):
        return await self._get(basePath + '/GroupV2/GetAvailableThemes/')
    
    async def getUserClanInviteSetting(self, mType, authorization):
        return await self._get(basePath + f'/GroupV2/GetUserClanInviteSetting/{mType}/', authorization=authorization)

    async def getRecommendedGroups(self, groupType, createDateRange, authorization):
        return await self._post(basePath + f'/GroupV2/Recommended/{groupType}/{createDateRange}/', None, authorization=authorization)

    async def groupSearch(self, data):
        return await self._post(basePath + '/GroupV2/Search/', data)
    
    async def getGroup(self, groupId):
        return await self._get(basePath + f'/GroupV2/{groupId}/')
    
    async def getGroupByName(self, groupName, groupType):
        return await self._get(basePath + f'/GroupV2/Name/{groupName}/{groupType}/')

    async def getGroupByNameV2(self, data):
        return await self._post(basePath + '/GroupV2/NameV2/', data)
    
    async def getGroupOptionalConversations(self, groupId):
        return await self._get(basePath + f'/GroupV2/{groupId}/OptionalConversations/')

    async def editGroup(self, groupId, data, authorization):
        return await self._post(basePath + f'/GroupV2/{groupId}/Edit/', data, authorization=authorization)

    async def editClanBanner(self, groupId, data, authorization):
        return await self._post(basePath + f'/GroupV2/{groupId}/EditClanBanner/', data, authorization=authorization)

    async def editFounderOptions(self, groupId, data, authorization):
        return await self._post(basePath + f'/GroupV2/{groupId}/EditFounderOptions/', data, authorization=authorization)

    async def addOptionalConversation(self, groupId, data, authorization):
        return await self._post(basePath + f'/GroupV2/{groupId}/OptionalConversations/Add/', data, authorization=authorization)

    async def editOptionalConversation(self, groupId, conversationId, data, authorization):
        return await self._post(basePath + f'/GroupV2/{groupId}/OptionalConversations/Edit/{conversationId}/', data, authorization=authorization)
    
    async def getMembersOfGroup(self, groupId, currentpage=1, memberType=None, nameSearch=None): # API reference says there should be pagination but no clue where, whoops
        return await self._get(basePath + f'/GroupV2/{groupId}/Members/', memberType=memberType, nameSearch=nameSearch)
    
    async def getAdminsAndFounderOfGroup(self, groupId, currentpage=1): # same :)
        return await self._get(basePath + f'/GroupV2/{groupId}/AdminsAndFounder/')

    async def editGroupMembership(self, groupId, membershipType, membershipId, memberType, authorization):
        return await self._post(basePath + f'/GroupV2/{groupId}/Members/{membershipType}/{membershipId}/SetMembershipType/{memberType}/', None, authorization=authorization)
    
    async def kickMember(self, groupId, membershipType, membershipId, authorization):
        return await self._post(basePath + f'/GroupV2/{groupId}/Members/{membershipType}/{membershipId}/Kick/', None, authorization=authorization)
    
    async def banMember(self, groupId, membershipType, membershipId, data, authorization):
        return await self._post(basePath + f'/GroupV2/{groupId}/Members/{membershipType}/{membershipId}/Ban/', data, authorization=authorization)
    
    async def unbanMember(self, groupId, membershipType, membershipId, authorization):
        return await self._post(basePath + f'/GroupV2/{groupId}/Members/{membershipType}/{membershipId}/Unban/', None, authorization=authorization)
    
    async def getBannedMembersOfGroup(self, groupId, currentpage=1): # .
        return await self._get(basePath + f'/GroupV2/{groupId}/Banned/')
    
    async def abdicateFoundership(self, groupId, membershipType, founderIdNew, authorization):
        return await self._post(basePath + f'/GroupV2/{groupId}/Admin/AbdicateFoundership/{membershipType}/{founderIdNew}/', None, authorization=authorization)
    
    async def getPendingMemberships(self, groupId, authorization, currentpage=1): # .
        return await self._get(basePath + f'/GroupV2/{groupId}/Members/Pending/', authorization=authorization)
    
    async def getInvitedIndividuals(self, groupId, authorization, currentpage=1): # .
        return await self._get(basePath + f'/GroupV2/{groupId}/Members/InvitedIndividuals/', authorization=authorization)
    
    async def approveAllPending(self, groupId, data, authorization):
        return await self._post(basePath + f'/GroupV2/{groupId}/Members/ApproveAll/', data, authorization=authorization)
    
    async def denyAllPending(self, groupId, data, authorization):
        return await self._post(basePath + f'/GroupV2/{groupId}/Members/DenyAll/', data, authorization=authorization)
    
    async def approvePendingForList(self, groupId, data, authorization):
        return await self._post(basePath + f'/GroupV2/{groupId}/Members/ApproveList/', data, authorization=authorization)
    
    async def approvePending(self, groupId, membershipType, membershipId, data, authorization):
        return await self._post(basePath + f'/GroupV2/{groupId}/Members/Approve/{membershipType}/{membershipId}/', data, authorization=authorization)
    
    async def denyPendingForList(self, groupId, data, authorization):
        return await self._post(basePath + f'/GroupV2/{groupId}/Members/DenyList/', data, authorization=authorization)
    
    async def getGroupsForMember(self, membershipType, membershipId, filter, groupType):
        return await self._get(basePath + f'/GroupV2/User/{membershipType}/{membershipId}/{filter}/{groupType}/')
    
    async def recoverGroupForFounder(self, membershipType, membershipId, groupType):
        return await self._get(basePath + f'/GroupV2/Recover/{membershipType}/{membershipId}/{groupType}/')
    
    async def getPotentialGroupsForMember(self, membershipType, membershipId, filter, groupType):
        return await self._get(basePath + f'/GroupV2/User/Potential/{membershipType}/{membershipId}/{filter}/{groupType}/')
    
    async def individualGroupInvite(self, groupId, membershipType, membershipId, data, authorization):
        return await self._post(basePath + f'/GroupV2/{groupId}/Members/IndividualInvite/{membershipType}/{membershipId}/', data, authorization=authorization)
    
    async def individualGroupInviteCancel(self, groupId, membershipType, membershipId, authorization):
        return await self._post(basePath + f'/GroupV2/{groupId}/Members/IndividualInviteCancel/{membershipType}/{membershipId}/', None, authorization=authorization)
    
    async def claimPartnerOffer(self, data, authorization):
        return await self._post(basePath + f'/Tokens/Partner/ClaimOffer/', data, authorization=authorization)
    
    async def applyMissingPartnerOffersWithoutClaim(self, partnerApplicationId, targetBnetMembershipId, authorization):
        return await self._post(basePath + f'/Tokens/Partner/ApplyMissingOffers/{partnerApplicationId}/{targetBnetMembershipId}/', None, authorization=authorization)
    
    async def getPartnerOfferSkuHistory(self, partnerApplicationId, targetBnetMembershipId, authorization):
        return await self._get(basePath + f'/Tokens/Partner/History/{partnerApplicationId}/{targetBnetMembershipId}/', authorization=authorization)
    
    async def getDestinyManifest(self):
        return await self._get(basePath + f'/Destiny2/Manifest/')
    
    async def getDestinyEntityDefinition(self, entityType, hashIdentifier):
        return await self._get(basePath + f'/Destiny2/Manifest/{entityType}/{hashIdentifier}/')
    
    async def searchDestinyPlayer(self, membershipType, displayName, returnOriginalProfile=False):
        return await self._get(basePath + f'/Destiny2/SearchDestinyPlayer/{membershipType}/{displayName}/', returnOriginalProfile=returnOriginalProfile)
    
    async def getLinkedProfiles(self, membershipType, membershipId, getAllMemberships=False):
        return await self._get(basePath + f'/Destiny2/{membershipType}/Profile/{membershipId}/LinkedProfiles/', getAllMemberships=getAllMemberships)
    
    async def getProfile(self, membershipType, destinyMembershipId, components):
        return await self._get(basePath + f'/Destiny2/{membershipType}/Profile/{destinyMembershipId}/', components=','.join(map(lambda c: str(int(c)),components)))
    
    async def getCharacter(self, membershipType, destinyMembershipId, characterId, components):
        return await self._get(basePath + f'/Destiny2/{membershipType}/Profile/{destinyMembershipId}/Character/{characterId}/', components=','.join(map(lambda c: str(int(c)),components)))
    
    async def getClanWeeklyRewardState(self, groupId):
        return await self._get(basePath + f'/Destiny2/Clan/{groupId}/WeeklyRewardState/')
    
    async def getItem(self, membershipType, destinyMembershipId, itemInstanceId, components):
        return await self._get(basePath + f'/Destiny2/{membershipType}/Profile/{destinyMembershipId}/Item/{itemInstanceId}/', components=','.join(map(lambda c: str(int(c)),components)))
    
    async def getVendors(self, membershipType, destinyMembershipId, characterId, components):
        return await self._get(basePath + f'/Destiny2/{membershipType}/Profile/{destinyMembershipId}/Character/{characterId}/Vendors/', components=','.join(map(lambda c: str(int(c)),components)))
    
    async def getVendor(self, membershipType, destinyMembershipId, characterId, vendorHash, components):
        return await self._get(basePath + f'/Destiny2/{membershipType}/Profile/{destinyMembershipId}/Character/{characterId}/Vendors/{vendorHash}/', components=','.join(map(lambda c: str(int(c)),components)))
    
    async def getCollectibleNodeDetails(self, membershipType, destinyMembershipId, characterId, collectiblePresentationNodeHash, components):
        return await self._get(basePath + f'/Destiny2/{membershipType}/Profile/{destinyMembershipId}/Character/{characterId}/Collectibles/{collectiblePresentationNodeHash}/', components=','.join(map(lambda c: str(int(c)),components)))
    
    async def transferItem(self, data, authorization):
        return await self._post(basePath + f'/Destiny2/Actions/Items/TransferItem/', data, authorization=authorization)
    
    async def pullFromPostmaster(self, data, authorization):
        return await self._post(basePath + f'/Destiny2/Actions/Items/PullFromPostmaster/', data, authorization=authorization)
    
    async def equipItem(self, data, authorization):
        return await self._post(basePath + f'/Destiny2/Actions/Items/EquipItem/', data, authorization=authorization)
    
    async def equipItem(self, data, authorization):
        return await self._post(basePath + f'/Destiny2/Actions/Items/EquipItems/', data, authorization=authorization)
    
    async def setItemLockState(self, data, authorization):
        return await self._post(basePath + f'/Destiny2/Actions/Items/SetLockState/', data, authorization=authorization)
    
    async def getPostGameCarnageReport(self, activityId):
        return await self._get(basePath + f'/Destiny2/Stats/PostGameCarnageReport/{activityId}/')
    
    async def reportOffensivePostGameCarnageReportPlayer(self, activityId, data, authorization):
        return await self._post(basePath + f'/Destiny2/Stats/PostGameCarnageReport/{activityId}/Report/', data, authorization=authorization)
    
    async def getHistoricalStatsDefinition(self):
        return await self._get(basePath + f'/Destiny2/Stats/Definition/')
    
    async def searchDestinyEntities(self, type, searchTerm, page=0):
        return await self._get(basePath + f'/Destiny2/Armory/Search/{type}/{searchTerm}/', page=page)
    
    async def getHistoricalStats(self, membershipType, destinyMembershipId, characterId, daystart, dayend, modes, groups=None, periodType=None):
        return await self._get(basePath + f'/Destiny2/{membershipType}/Account/{destinyMembershipId}/Character/{characterId}/Stats/', daystart=daystart, dayend=dayend, modes=modes, groups=groups, periodType=periodType)
    
    async def getHistoricalStatsForAccount(self, membershipType, destinyMembershipId, groups=None):
        return await self._get(basePath + f'/Destiny2/{membershipType}/Account/{destinyMembershipId}/Stats/', groups=groups)
    
    async def getActivityHistory(self, membershipType, destinyMembershipId, characterId, count=None, mode=None, page=0):
        return await self._get(basePath + f'/Destiny2/{membershipType}/Account/{destinyMembershipId}/Character/{characterId}/Stats/Activities/', count=count, mode=mode, page=page)
    
    async def getUniqueWeaponHistory(self, membershipType, destinyMembershipId, characterId):
        return await self._get(basePath + f'/Destiny2/{membershipType}/Account/{destinyMembershipId}/Character/{characterId}/Stats/UniqueWeapons/')
    
    async def getDestinyAggregateActivityStats(self, membershipType, destinyMembershipId, characterId):
        return await self._get(basePath + f'/Destiny2/{membershipType}/Account/{destinyMembershipId}/Character/{characterId}/Stats/AggregateActivityStats/')
    
    async def getPublicMilestoneContent(self, milestoneHash):
        return await self._get(basePath + f'/Destiny2/Milestones/{milestoneHash}/Content/')
    
    async def getPublicMilestones(self):
        return await self._get(basePath + f'/Destiny2/Milestones/')
    
    async def awaInitializeRequest(self, data, authorization):
        return await self._post(basePath + f'/Destiny2/Awa/Initialize/', data, authorization=authorization)
    
    async def awaProvideAuthorizationResult(self, data, authorization):
        return await self._post(basePath + f'/Destiny2/Awa/AwaProvideAuthorizationResult/', data, authorization=authorization)
    
    async def awaGetActionToken(self, correlationId, authorization):
        return await self._get(basePath + f'/Destiny2/Awa/GetActionToken/{correlationId}/', authorization=authorization)
    
    async def getCommunityContent(self, sort, mediaFilter, page):
        return await self._get(basePath + f'/CommunityContent/Get/{sort}/{mediaFilter}/{page}/')
    
    async def getTrendingCategories(self):
        return await self._get(basePath + f'/Trending/Categories/')
    
    async def getTrendingCategory(self, categoryId, pageNumber):
        return await self._get(basePath + f'/Trending/Categories/{categoryId}/{pageNumber}/')
    
    async def getTrendingEntryDetail(self, trendingEntryType, identifier):
        return await self._get(basePath + f'/Trending/Details/{trendingEntryType}/{identifier}/')
    
    async def getActivePrivateClanFireteamCount(self, groupId, authorization):
        return await self._get(basePath + f'/Fireteam/Clan/{groupId}/ActiveCount/', authorization=authorization)
    
    async def getAvailableClanFireteams(self, groupId, platform, activityType, dateRange, slotFilter, publicOnly, page, authorization, langFilter=None):
        return await self._get(basePath + f'/Fireteam/Clan/{groupId}/Available/{platform}/{activityType}/{dateRange}/{slotFilter}/{publicOnly}/{page}/', langFilter=langFilter, authorization=authorization)

    async def searchPublicAvailableClanFireteams(self, platform, activityType, dateRange, slotFilter, page, authorization, langFilter=None):
        return await self._get(basePath + f'/Fireteam/Search/Available/{platform}/{activityType}/{dateRange}/{slotFilter}/{page}/', langFilter=langFilter, authorization=authorization)
    
    async def getMyClanFireteams(self, groupId, platform, includeClosed, page, groupFilter, authorization, langFilter=None):
        return await self._get(basePath + f'/Fireteam/Clan/{groupId}/My/{platform}/{includeClosed}/{page}/', langFilter=langFilter, groupFilter=groupFilter, authorization=authorization)
    
    async def getClanFireteam(self, groupId, fireteamId, authorization):
        return await self._get(basePath + f'/Fireteam/Clan/{groupId}/Summary/{fireteamId}/', authorization=authorization)
    
    async def getAvailableLocales(self):
        return await self._get(basePath + f'/GetAvailableLocales/')
    
    async def getCommonSettings(self):
        return await self._get(basePath + f'/Settings/')
    
    async def getGlobalAlerts(self, includestreaming):
        return await self._get(basePath + f'/GlobalAlerts/', includestreaming=includestreaming)

