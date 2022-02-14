import json
from sqlalchemy.orm import DeclarativeMeta



class AlchemyEncoder(json.JSONEncoder):

    async def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):

            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data)
                    fields[field] = data
                except TypeError:
                    fields[field] = None

            return fields

        return json.JSONEncoder.default(self, obj)


class User:
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}