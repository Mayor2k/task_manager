from sqlalchemy.orm import Session
from sqlalchemy.future import select

import models, schemas

class Crud():
    def __init__(self, db_session: Session):
        self.db_session = db_session
        
    async def get_models(self, model: object, skip: int = 0, limit: int = 100):
        query = await self.db_session.execute(select(model).offset(skip).limit(limit).order_by(model.id))
        return query.scalars().all()
    
    async def get_model(self, model: object, model_id: int):
        query = await self.db_session.execute(select(model).filter(model.id == model_id))
        return query.scalars().first()
    
    async def create_model(self, model: object, data: dict):
        db_model = model(**data)
        self.db_session.add(db_model)
        await self.db_session.flush()
        await self.db_session.refresh(db_model)  
        return db_model
    
    async def delete_model(self, model: object, model_id: int):
        db_model = await self.get_model(model = model, model_id = model_id)
        if not db_model:
            return False
        await self.db_session.delete(db_model)
        await self.db_session.flush()
        return True
    
    async def update_model(self, model: object, model_id: int, data: dict):
        db_model = await self.get_model(model = model, model_id = model_id)
        if db_model:
            for key, value in data.items():
                if value is None:
                    continue
                setattr(db_model, key, value)
            await self.db_session.commit()
            return db_model
        return False
        
class UserCrud(Crud):
        
    async def get_models(self, model = models.User, skip: int = 0, limit: int = 100):
        return await super().get_models(model = model, skip = skip , limit = limit)
        
    async def get_model(self, model_id: int, model = models.User):
        return await super().get_model(model = model, model_id = model_id)
    
    async def create_model(self, data: schemas.UserCreate, model = models.User):
        data = data.dict()
        #create imitation of a hashed password  
        data['hashed_password'] = data['password'] + "notreallyhashed"
        del data['password']
        
        return await super().create_model(model = model, data = data)
    
    async def delete_model(self, model_id: int, model = models.User):
        return await super().delete_model(model, model_id)
    
    async def update_model(self, model_id: int, data: dict, model = models.User):
        return await super().update_model(model = model, model_id = model_id, data = data.dict())

    async def get_model_by_email(self, email: str):
        query = await self.db_session.execute(select(models.User).filter(models.User.email == email))
        return query.scalars().first()

class TaskCrud(Crud):
        
    async def get_models(self, skip: int = 0, limit: int = 100, model = models.Task):
        return await super().get_models(model = model, skip = skip , limit = limit)
        
    async def get_model(self, model: models.Task, model_id: int):
        return await super().get_model(model = model, model_id = model_id)
    
    async def create_model(self, data: schemas.Task, model = models.Task):
        return await super().create_model(model = model, data = data.dict())
    
    async def delete_model(self, model_id: int, model = models.Task):
        return await super().delete_model(model = model, model_id = model_id)
    
    async def update_model(self, model_id: int, data: dict, model = models.Task):
        return await super().update_model(model = model, model_id = model_id, data = data.dict())