from enum import Enum

class AboutInfoStatus(str, Enum):
    ACTIVE='ACTIVE'
    INACTIVE='INACTIVE'

class EventStatus(str, Enum):
    ACTIVE='ACTIVE'
    INACTIVE='INACTIVE'

class FaqStatus(str, Enum):
    ACTIVE='ACTIVE'
    INACTIVE='INACTIVE'

class LandingPageBannerStatus(str, Enum):
    ACTIVE='ACTIVE'
    INACTIVE='INACTIVE'

class PartnerPromotionStatus(str, Enum):
    ACTIVE='ACTIVE'
    INACTIVE='INACTIVE'

class SponsorStatus(str, Enum):
    ACTIVE='ACTIVE'
    INACTIVE='INACTIVE'

class SupportingPartnerStatus(str, Enum):
    ACTIVE='ACTIVE'
    INACTIVE='INACTIVE'

class UpdatesSubscriberStatus(str, Enum):
    SUBSCRIBE_RECEIVED='SUBSCRIBE_RECEIVED'
    SUBSCRIBE_SENT='SUBSCRIBE_SENT'
    UNSUBSCRIBE_RECEIVED='UNSUBSCRIBE_RECEIVED'
    UNSUBSCRIBE_SENT='UNSUBSCRIBE_SENT'

class SponsorStatus(str, Enum):
    ACTIVE='ACTIVE'
    INACTIVE='INACTIVE'

class DynamoDBStreamEventName(str, Enum):
    INSERT='INSERT'
    REMOVE='REMOVE'
    MODIFY='MODIFY'
    MODIFY_OLD='MODIFY_OLD'
    MODIFY_NEW='MODIFY_NEW'
