from fastapi import APIRouter, HTTPException, Depends
from typing import List
from models.task import Task
from db import get_database
from bson.objectid import ObjectId
from pymongo import ReturnDocument
import logging

router = APIRouter()


@router.post("/", response_model=Task)
async def create_task(task: Task, db=Depends(get_database)):
    try:
        await db.tasks.insert_one(task.dict())
        return task
    except Exception as e:
        logging.error(f"Error creating task: {e}")
        raise HTTPException(status_code=500, detail="Failed to create task")


@router.get("/", response_model=List[Task])
async def get_tasks(db=Depends(get_database)):
    try:
        tasks = await db.tasks.find().to_list(1000)
        return [
            Task(
                title=t["title"],
                description=t.get("description"),
                completed=t.get("completed", False),
            )
            for t in tasks
        ]
    except Exception as e:
        logging.error(f"Error fetching tasks: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch tasks")


@router.put("/{task_id}", response_model=Task)
async def update_task(task_id: str, task: Task, db=Depends(get_database)):
    try:
        updated_task = await db.tasks.find_one_and_update(
            {"_id": ObjectId(task_id)},
            {"$set": task.dict()},
            return_document=ReturnDocument.AFTER,
        )

        if updated_task is None:
            raise HTTPException(status_code=404, detail="Task not found")

        return Task(
            title=updated_task["title"],
            description=updated_task.get("description"),
            completed=updated_task.get("completed", False),
        )
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error updating task: {e}")
        raise HTTPException(status_code=500, detail="Failed to update task")


@router.delete("/{task_id}")
async def delete_task(task_id: str, db=Depends(get_database)):
    try:
        delete_result = await db.tasks.delete_one({"_id": ObjectId(task_id)})

        if delete_result.deleted_count == 1:
            return {"message": "Task deleted"}

        raise HTTPException(status_code=404, detail="Task not found")
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error deleting task: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete task")
