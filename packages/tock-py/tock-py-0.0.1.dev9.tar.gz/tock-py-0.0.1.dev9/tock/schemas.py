# -*- coding: utf-8 -*-
from marshmallow import Schema, fields, EXCLUDE, post_load, post_dump
from marshmallow.fields import String
from marshmallow_enum import EnumField
from marshmallow_oneofschema import OneOfSchema

from tock.models import TockMessage, BotRequest, User, UserId, ConnectorType, \
    Message, Entity, RequestContext, BotResponse, ResponseContext, \
    Sentence, I18nText, Suggestion, PlayerType, Card, AttachmentType, \
    Attachment, Action, Carousel, StoryConfiguration, \
    StepConfiguration, ClientConfiguration


def camelcase(s):
    parts = iter(s.split("_"))
    return next(parts) + "".join(i.title() for i in parts)


class TockSchema(Schema):
    SKIP_VALUES = {None}

    def on_bind_field(self, field_name, field_obj):
        field_obj.data_key = camelcase(field_obj.data_key or field_name)

    @post_dump
    def remove_skip_values(self, data, many, **kwargs):
        return {
            key: value for key, value in data.items()
            if value is not None
            # if value not in self.SKIP_VALUES
        }

    class Meta:
        unknown = EXCLUDE
        datetimeformat = '%Y-%m-%dT%H:%M:%SZ'
        ordered = True


class EntitySchema(TockSchema):
    type = fields.String(required=True)
    role = fields.String(required=True)
    content = fields.String(required=False)
    value = fields.String(required=False)
    evaluated = fields.Boolean(required=True)
    # subEntities = fields.List(fields.Nested(EntitySchema), required=True)
    new = fields.Boolean(required=True)

    @post_load
    def make_entity(self, data, **kwargs):
        return Entity(**data)


class MessageSchema(TockSchema):
    type = fields.String(required=True)
    text = fields.String(required=True)

    @post_load
    def make_message(self, data, **kwargs):
        return Message(**data)


class ConnectorTypeSchema(TockSchema):
    id = fields.String(required=True)
    user_interface_type = fields.String(required=True)

    @post_load
    def make_connector_type(self, data, **kwargs):
        return ConnectorType(**data)


class UserIdSchema(TockSchema):
    id = fields.String(required=True)
    type = EnumField(PlayerType, by_value=True)
    client_id = fields.String(required=False, allow_none=True)

    @post_load
    def make_user_id(self, data, **kwargs):
        return UserId(**data)


class UserSchema(TockSchema):
    timezone = fields.String(required=True)
    locale = fields.String(required=True)
    test = fields.Boolean(required=True)

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)


class RequestContextSchema(TockSchema):
    namespace = fields.String(required=True)
    language = fields.String(required=True)
    connector_type = fields.Nested(ConnectorTypeSchema)
    user_interface = fields.String(required=True)
    application_id = fields.String(required=True)
    user_id = fields.Nested(UserIdSchema)
    bot_id = fields.Nested(UserIdSchema)
    user = fields.Nested(UserSchema)

    @post_load
    def make_request_context(self, data, **kwargs):
        return RequestContext(**data)


class I18NTextSchema(TockSchema):
    text = fields.String(required=True)
    args = fields.List(fields.String, required=True)
    to_be_translated = fields.Boolean(required=True)
    length = fields.Integer(required=True)
    key = fields.String(required=False)

    @post_load
    def make_i18n_text(self, data, **kwargs):
        return I18nText(**data)


class SuggestionSchema(TockSchema):
    title = fields.Nested(I18NTextSchema, required=True)

    @post_load
    def make_suggestion(self, data, **kwargs):
        return Suggestion(**data)


class AttachmentSchema(TockSchema):
    url = fields.String(required=True)
    type = EnumField(AttachmentType, by_value=True, required=False)

    @post_load
    def make_attachment(self, data, **kwargs):
        return Attachment(**data)


class ActionSchema(TockSchema):
    title = fields.Nested(I18NTextSchema)
    url = fields.String(required=False)

    @post_load
    def make_suggestion(self, data, **kwargs):
        return Action(**data)


class BotMessageSchema(TockSchema):
    delay = fields.Integer(required=False)


class SentenceSchema(BotMessageSchema):
    text = fields.Nested(I18NTextSchema)
    suggestions = fields.List(fields.Nested(SuggestionSchema), required=True)

    @post_load
    def make_sentence(self, data, **kwargs):
        return Sentence(**data)


class CardSchema(BotMessageSchema):
    title = fields.Nested(I18NTextSchema, required=False)
    sub_title = fields.Nested(I18NTextSchema, required=False)
    attachment = fields.Nested(AttachmentSchema, required=False)
    actions = fields.List(fields.Nested(ActionSchema), required=True)

    @post_load
    def make_card(self, data, **kwargs):
        return Card(**data)


class UberCardSchema(OneOfSchema):
    type_field = "type"
    type_schemas = {"card": CardSchema}

    def get_obj_type(self, obj):
        if isinstance(obj, Card):
            return "card"
        else:
            raise Exception("Unknown object type: {}".format(obj.__class__.__name__))


class CarouselSchema(BotMessageSchema):
    cards = fields.List(fields.Nested(UberCardSchema), required=True)

    @post_load
    def make_carousel(self, data, **kwargs):
        return Carousel(**data)


class UberBotMessageSchema(OneOfSchema):
    type_field = "type"
    type_schemas = {"sentence": SentenceSchema, "card": CardSchema, "carousel": CarouselSchema}

    def get_obj_type(self, obj):
        if isinstance(obj, Sentence):
            return "sentence"
        elif isinstance(obj, Card):
            return "card"
        elif isinstance(obj, Carousel):
            return "carousel"
        else:
            raise Exception("Unknown object type: {}".format(obj.__class__.__name__))


class ResponseContextSchema(TockSchema):
    request_id = fields.String(required=True)
    date = fields.DateTime(required=True)

    @post_load
    def make_response_context(self, data, **kwargs):
        return ResponseContext(**data)


class BotRequestSchema(TockSchema):
    intent = fields.String(required=True)
    entities = fields.List(fields.Nested(EntitySchema), required=True)
    message = fields.Nested(MessageSchema())
    story_id = fields.String(required=True)
    context = fields.Nested(RequestContextSchema, required=False)

    @post_load
    def make_bot_request(self, data, **kwargs):
        return BotRequest(**data)


class BotResponseSchema(TockSchema):
    messages = fields.List(fields.Nested(UberBotMessageSchema), required=True)
    story_id = fields.String(required=True)
    step = fields.String(required=False)
    entities = fields.List(fields.Nested(EntitySchema), required=True)
    context = fields.Nested(ResponseContextSchema, required=True)

    @post_load
    def make_bot_response(self, data, **kwargs):
        return BotResponse(**data)


class StepConfigurationSchema(TockSchema):
    main_intent = fields.String(required=True)
    name = fields.String(required=True)
    other_starter_intents = fields.List(String, required=True)
    secondary_intents = fields.List(String, required=True)

    @post_load
    def make_step_configuration(self, data, **kwargs):
        return StepConfiguration(**data)


class StoryConfigurationSchema(TockSchema):
    main_intent = fields.String(required=True)
    name = fields.String(required=True)
    other_starter_intents = fields.List(String, required=True)
    secondary_intents = fields.List(String, required=True)
    steps = fields.List(fields.Nested(StepConfigurationSchema), required=True)

    @post_load
    def make_story_configuration(self, data, **kwargs):
        return StoryConfiguration(**data)


class ClientConfigurationSchema(TockSchema):
    stories = fields.List(fields.Nested(StoryConfigurationSchema), required=True)

    @post_load
    def make_client_configuration(self, data, **kwargs):
        return ClientConfiguration(**data)


class TockMessageSchema(TockSchema):
    bot_request = fields.Nested(BotRequestSchema, required=False)
    bot_response = fields.Nested(BotResponseSchema, required=False)
    bot_configuration = fields.Nested(ClientConfigurationSchema, required=False)
    configuration = fields.Boolean(required=False)
    request_id = fields.String(required=True)

    @post_load
    def make_tockmessage(self, data, **kwargs):
        return TockMessage(**data)


class UnsupportedSchema:
    pass
