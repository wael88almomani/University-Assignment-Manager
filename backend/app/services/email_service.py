from app.core.email_service import SMTPEmailService


class NotificationService:
    def __init__(self, email_service: SMTPEmailService):
        self.email_service = email_service

    def notify_assignment_created(self, to_email: str, assignment_title: str) -> None:
        self.email_service.send_email(
            to_email=to_email,
            subject="New Assignment Created",
            body=f"A new assignment has been created: {assignment_title}",
        )

    def notify_submission_uploaded(self, to_email: str, assignment_title: str) -> None:
        self.email_service.send_email(
            to_email=to_email,
            subject="Submission Uploaded",
            body=f"A submission was uploaded for assignment: {assignment_title}",
        )

    def notify_grade_assigned(self, to_email: str, assignment_title: str, grade: float) -> None:
        self.email_service.send_email(
            to_email=to_email,
            subject="Grade Assigned",
            body=f"A grade was assigned for {assignment_title}: {grade}",
        )
