from django.core.exceptions import ValidationError


class ContainsLetterValidator:
    """
    Validator class for ensuring that a password contains at least one letter (uppercase or lowercase).
    """

    def validate(self, password, user=None):
        """
        Validates the password to ensure it contains at least one letter.

        Args:
            password (str): The password to be validated.
            user (User, optional): The user object. Defaults to None.

        Raises:
            ValidationError: If the password does not contain a letter, a validation error is raised.
        """
        if not any(char.isalpha() for char in password):
            raise ValidationError(
                'Le mot de passe doit contenir une lettre',
                code='password_no_letters',
            )

    def get_help_text(self):
        """
        Returns the help text for the password validation.

        Returns:
            str: The help text message.
        """
        return 'Votre mot de passe doit contenir au moins une lettre majuscule ou minuscule.'


class ContainsNumberValidator:
    """
    Validator class for ensuring that a password contains at least one digit.
    """

    def validate(self, password, user=None):
        """
        Validates the password to ensure it contains at least one digit.

        Args:
            password (str): The password to be validated.
            user (User, optional): The user object. Defaults to None.

        Raises:
            ValidationError: If the password does not contain a digit, a validation error is raised.
        """
        if not any(char.isdigit() for char in password):
            raise ValidationError(
                'Le mot de passe doit contenir un chiffre',
                code='password_no_number',
            )

    def get_help_text(self):
        """
        Returns the help text for the password validation.

        Returns:
            str: The help text message.
        """
        return 'Votre mot de passe doit contenir au moins un chiffre.'
