from app.model import VacationModel
from app.repository.base import BaseRepository


class _VacationRepository(BaseRepository):
    def filter(self, session, equal, gte, lte, ne):
        filters = [getattr(self.model, k) == v for k, v in equal.items()] \
                  + [getattr(self.model, k) >= v for k, v in gte.items()] \
                  + [getattr(self.model, k) <= v for k, v in lte.items()] \
                  + [getattr(self.model, k) != v for k, v in ne.items()]
        return session.query(self.model).filter(*filters).all()


VacationRepository = _VacationRepository(model=VacationModel)
