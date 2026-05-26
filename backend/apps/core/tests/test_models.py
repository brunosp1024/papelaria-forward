from apps.core.models.person import Person


class ConcretePerson(Person):
    class Meta:
        app_label = "core"


def test_person_str():
    person = ConcretePerson(name="Test")
    assert str(person) == "Test"
