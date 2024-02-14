from django import forms

def user_file_upload_path(instance, filename):
    return "{0}/{1}".format(instance.user.id, filename)


def validate_file(
    file, allowed_extensions=["pdf"], max_size=10 * 1024 * 1024
):
    if file:
        # Check the file extension
        file_extension = file.name.split(".")[-1]
        if file_extension not in allowed_extensions:
            raise forms.ValidationError(
                "File type not supported. Allowed formats: pdf"
            )

        # Check the file size
        if file.size > max_size:
            raise forms.ValidationError(
                f"File size is too large. Max file size is {max_size / (1024 * 1024)}MB."
            )

    return file
