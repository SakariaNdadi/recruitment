from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.core import mail
from .models import Application, Interview


@receiver(post_save, sender=Application)
def send_vacancy_application_notification_email(sender, instance, created, **kwargs):
    if not created and instance.status == "shortlisted":
        subject = f"{instance.vacancy} Application Status"
        message = f"""
            Dear {instance.user.profile.first_name} {instance.user.profile.last_name},

            I trust this email finds you well. We appreciate the time and effort you invested in your application for the {instance.vacancy} role at Telecom Namibia Limited. After careful consideration, we are pleased to inform you that you have been shortlisted for the next stage of our selection process.

            We were impressed with your qualifications and experience, which align well with the requirements of the position. We would like to learn more about your skills and discuss how your expertise could contribute to our team.

            Further details regarding the next steps in the hiring process will be communicated to you shortly. This may include additional assessments, interviews, or other relevant procedures. We aim to keep you informed at every stage, ensuring a transparent and efficient process.

            Once again, congratulations on reaching this stage, and we look forward to the opportunity to get to know you better.

            If you have any questions or require additional information in the meantime, please feel free to contact us at training@telecom.na.

            Best regards,

            Mr OG Heitha

        """
        from_email = "training@telecom.na"
        recipient_list = [instance.user.email]

        send_mail(subject, message, from_email, recipient_list)

    if not created and instance.status == "rejected":
        subject = f"{instance.vacancy} Application Status"
        message = f"""
            Dear {instance.user.profile.first_name} {instance.user.profile.last_name},
            
            I hope this message finds you well. Thank you for your interest in the {instance.vacancy} position at Telecom Namibia Limited. We appreciate the time and effort you dedicated to the application process.
            
            After careful consideration, we regret to inform you that we have chosen not to move forward with your application at this time. We received a high volume of qualified applicants, and our decision-making process was challenging due to the exceptional caliber of candidates.

            We want to express our gratitude for your interest in joining our team. Your skills and experience are valued, and we encourage you to apply for future opportunities that align with your professional background.

            We understand that this news may be disappointing, and we wish you continued success in your job search. If you have any specific feedback or questions about your application, please feel free to reach out to us.

            Thank you once again for considering Telecom Namibia Limited as a potential employer. We appreciate the opportunity to connect with you during this process.

            Wishing you all the best in your future endeavors.

            Sincerely,

            Mr. OG Heitha
        """
        from_email = "training@telecom.na"
        recipient_list = [instance.user.email]

        send_mail(subject, message, from_email, recipient_list)


@receiver(post_save, sender=Interview)
def send_interview_notification_email(sender, instance, created, **kwargs):
    if not created and instance.status == "scheduled":
        subject = f"{instance.application.vacancy} Application Interview"
        message = f"""
            Dear {instance.application.user.profile.first_name} {instance.application.user.profile.last_name},

            I hope this email finds you well. We appreciate your interest in the {instance.application.vacancy} position at Telecom Namibia Limited. We are pleased to invite you for an interview to discuss your candidacy further.

            Interview Details:

            Date and Time: {instance.dateTime}
            Type of interview: {instance.interview_type}
            Duration: {instance.duration}
            Location: {instance.location}

            If the scheduled time is inconvenient or if you have any specific requests, please let us know as soon as possible, and we will do our best to accommodate.

            We look forward to the opportunity to learn more about you and discuss how your expertise can contribute to our team. Please confirm your attendance by replying to this email.

            If you have any questions or need further information, feel free to contact us at training@telecom.na.

            Thank you for your interest in Telecom Namibia Limited, and we look forward to meeting you.

            Best regards,

            Mr. OG Heitha
        """
        from_email = "training@telecom.na"
        recipient_list = [instance.application.user.email]

        send_mail(subject, message, from_email, recipient_list)
