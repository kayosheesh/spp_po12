"""Simple hospital domain model with staff, patients and prescriptions."""

# pylint: disable=too-few-public-methods

from __future__ import annotations

from abc import ABC, abstractmethod


class Person:
    """Base entity for people in the hospital system."""

    def __init__(self, name: str) -> None:
        self.name = name

    def __str__(self) -> str:
        return f"{self.__class__.__name__}: {self.name}"


class MedicalStaff(Person):  # pylint: disable=too-few-public-methods
    """Marker base class for all medical workers."""


class Doctor(MedicalStaff):
    """Doctor that can create treatment prescriptions for patients."""

    def prescribe(self, target_patient: Patient, description: str) -> Prescription:
        """Create and attach a prescription to the provided patient."""
        treatment = Prescription(description, self, target_patient)
        target_patient.add_prescription(treatment)
        return treatment


class Nurse(MedicalStaff):  # pylint: disable=too-few-public-methods
    """Nurse role in the hospital."""


class Patient(Person):
    """Patient with treatment list and discharge status."""

    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.prescriptions: list[Prescription] = []
        self.is_discharged = False
        self.discharge_reason: str | None = None

    def add_prescription(self, treatment: Prescription) -> None:
        """Attach a new prescription to the patient."""
        self.prescriptions.append(treatment)

    def discharge(self, reason: str) -> None:
        """Discharge patient and store discharge reason."""
        self.is_discharged = True
        self.discharge_reason = reason

    def __str__(self) -> str:
        status = "Выписан" if self.is_discharged else "На лечении"
        return f"Пациент: {self.name}, статус: {status}"


class Executable(ABC):
    """Interface for entities that can be executed by performer."""

    @abstractmethod
    def execute(self, performer: MedicalStaff) -> None:
        """Execute action by the given medical performer."""
        raise NotImplementedError


class Prescription(Executable):
    """Treatment instruction created by doctor for patient."""

    def __init__(self, description: str, doctor: Doctor, patient: Patient) -> None:
        self.description = description
        self.doctor = doctor
        self.patient = patient
        self.is_executed = False

    def execute(self, performer: MedicalStaff) -> None:
        """Mark the prescription as executed by a medical staff member."""
        if not isinstance(performer, MedicalStaff):
            raise ValueError("Исполнитель должен быть медицинским персоналом")
        self.is_executed = True
        print(f"{performer.name} выполнил назначение: {self.description}")

    def __str__(self) -> str:
        status = "Выполнено" if self.is_executed else "Не выполнено"
        return f"Назначение: {self.description} ({status})"


class Hospital:
    """Hospital aggregate that stores staff and patients."""

    def __init__(self, name: str) -> None:
        self.name = name
        self.patients: list[Patient] = []
        self.staff: list[MedicalStaff] = []

    def add_patient(self, patient: Patient) -> None:
        """Add patient to hospital records."""
        self.patients.append(patient)

    def add_staff(self, staff_member: MedicalStaff) -> None:
        """Add medical staff member to hospital records."""
        self.staff.append(staff_member)

    def __str__(self) -> str:
        return (
            f"Больница: {self.name}, пациентов: {len(self.patients)}, "
            f"персонала: {len(self.staff)}"
        )


def main() -> None:
    """Run a small usage demo for the model."""
    city_hospital = Hospital("Городская больница")

    main_doctor = Doctor("Иванов")
    duty_nurse = Nurse("Петрова")
    admitted_patient = Patient("Сидоров")

    city_hospital.add_staff(main_doctor)
    city_hospital.add_staff(duty_nurse)
    city_hospital.add_patient(admitted_patient)

    print(city_hospital)

    treatment = main_doctor.prescribe(admitted_patient, "Прием антибиотиков")
    print(treatment)

    treatment.execute(duty_nurse)
    print(treatment)

    admitted_patient.discharge("Окончание лечения")
    print(admitted_patient)


if __name__ == "__main__":
    main()
