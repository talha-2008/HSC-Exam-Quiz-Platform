import reflex as rx
import asyncio
import random
from datetime import datetime
from typing import TypedDict
from app.states.data import questions, Question
from app.states.auth_state import AuthState, User
import json


class WrongAnswer(TypedDict):
    question: str
    selected: str
    correct: str
    options: list[str]


class QuizResult(TypedDict):
    subject: str
    score: int
    total: int
    percentage: float
    date: str
    wrong_answers: list[WrongAnswer]


class QuizState(rx.State):
    current_subject: str = ""
    current_questions: list[Question] = []
    current_question_index: int = 0
    selected_answers: dict[int, str] = {}
    quiz_in_progress: bool = False
    quiz_submitted: bool = False
    time_left: int = 1200
    timer_active: bool = False
    last_result: QuizResult | None = None

    async def check_login(self):
        auth_state = await self.get_state(AuthState)
        if not auth_state.is_logged_in:
            return rx.redirect("/login")

    @rx.var
    def formatted_time_left(self) -> str:
        minutes = self.time_left // 60
        seconds = self.time_left % 60
        return f"{minutes}:{seconds:02d}"

    @rx.var
    def subjects(self) -> list[str]:
        return list(questions.keys())

    @rx.var
    async def quiz_history(self) -> list[QuizResult]:
        auth_state = await self.get_state(AuthState)
        if auth_state.current_user_data:
            return auth_state.current_user_data.get("quiz_history", [])
        return []

    @rx.var
    async def total_quizzes_taken(self) -> int:
        history = await self.quiz_history
        return len(history)

    @rx.var
    async def best_score(self) -> float:
        history = await self.quiz_history
        if not history:
            return 0.0
        return max([result["percentage"] for result in history] or [0.0])

    @rx.var
    async def average_percentage(self) -> float:
        history = await self.quiz_history
        if not history:
            return 0.0
        total_percentage = sum([result["percentage"] for result in history])
        return round(total_percentage / len(history), 2)

    @rx.var
    async def performance_data(self) -> list[dict]:
        history = await self.quiz_history
        return [{"date": res["date"], "score": res["percentage"]} for res in history]

    @rx.var
    def quiz_history_for_chart(self) -> list[dict]:
        return []

    @rx.var
    def result_pie_data(self) -> list[dict]:
        if not self.last_result:
            return []
        correct = self.last_result["score"]
        wrong = self.last_result["total"] - correct
        return [
            {"name": "Correct", "value": correct, "fill": "#22c55e"},
            {"name": "Wrong", "value": wrong, "fill": "#ef4444"},
        ]

    def _get_random_questions(
        self, subject: str, num_questions: int = 10
    ) -> list[Question]:
        all_questions = questions.get(subject, [])
        return random.sample(all_questions, min(num_questions, len(all_questions)))

    def start_quiz(self, subject: str):
        self.current_subject = subject
        self.current_questions = self._get_random_questions(subject)
        self.current_question_index = 0
        self.selected_answers = {}
        self.quiz_in_progress = True
        self.quiz_submitted = False
        self.time_left = 1200
        self.timer_active = True
        return self.tick

    def select_answer(self, question_index: int, answer: str):
        self.selected_answers[question_index] = answer

    def next_question(self):
        if self.current_question_index < len(self.current_questions) - 1:
            self.current_question_index += 1

    def prev_question(self):
        if self.current_question_index > 0:
            self.current_question_index -= 1

    @rx.event(background=True)
    async def tick(self):
        while True:
            async with self:
                if not self.timer_active or not self.quiz_in_progress:
                    break
                if self.time_left > 0:
                    self.time_left -= 1
                else:
                    self.timer_active = False
                    yield QuizState.submit_quiz
                    break
            await asyncio.sleep(1)

    async def _update_dashboard_data(self):
        auth_state = await self.get_state(AuthState)
        if not auth_state.is_logged_in:
            return
        user_data = auth_state.current_user_data
        history = user_data.get("quiz_history", [])
        self.quiz_history_for_chart = [
            {"date": res["date"], "score": res["percentage"]} for res in history
        ]

    @rx.event
    async def submit_quiz(self):
        if not self.quiz_in_progress:
            return
        self.timer_active = False
        self.quiz_in_progress = False
        score = 0
        wrong_answers: list[WrongAnswer] = []
        for i, q in enumerate(self.current_questions):
            if self.selected_answers.get(i) == q["answer"]:
                score += 1
            else:
                wrong_answers.append(
                    {
                        "question": q["question"],
                        "selected": self.selected_answers.get(i, "Not Answered"),
                        "correct": q["answer"],
                        "options": q["options"],
                    }
                )
        total = len(self.current_questions)
        percentage = round(score / total * 100, 2) if total > 0 else 0
        date_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.last_result = {
            "subject": self.current_subject,
            "score": score,
            "total": total,
            "percentage": percentage,
            "date": date_str,
            "wrong_answers": wrong_answers,
        }
        self.quiz_submitted = True
        auth_state = await self.get_state(AuthState)
        if auth_state.is_logged_in:
            user_data = auth_state.current_user_data
            if user_data:
                new_history = user_data.get("quiz_history", []) + [self.last_result]
                user_data["quiz_history"] = new_history
                all_users = auth_state.users
                all_users[auth_state.logged_in_user] = user_data
                auth_state.users_json = json.dumps(all_users)
        await self._update_dashboard_data()

    @rx.event
    async def go_home(self):
        self.quiz_in_progress = False
        self.quiz_submitted = False
        self.current_subject = ""
        self.timer_active = False
        await self._update_dashboard_data()