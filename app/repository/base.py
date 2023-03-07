class BaseRepository:
    def __init__(self, model):
        self.model = model

    def _query(self, session, *_, **kwargs):
        filters = [getattr(self.model, k) == v for k, v in kwargs.items()]
        return session.query(self.model).filter(*filters)

    def get(self, session, *_, **kwargs):
        return self._query(session, **kwargs).one_or_none()

    def get_many(self, session, *_, **kwargs):
        return self._query(session, **kwargs).all()

    def create(self, session, obj_in):
        obj = self.model(**obj_in.dict())
        session.add(obj)
        session.commit()
        return obj

    def delete(self, session, *_, **kwargs):
        obj = self.get(session, **kwargs)
        if obj:
            session.delete(obj)
            session.commit()
            return True
        return False

    def update(self, session, obj_id, obj_in):
        obj = session.query(self.model).filter(self.model.id == obj_id)
        if not obj:
            return False
        obj_data = obj_in.dict(exclude_unset=True)
        for key, value in obj_data.items():
            setattr(obj, key, value)
        session.add(obj)
        session.commit()
        session.refresh(obj)
        return obj
