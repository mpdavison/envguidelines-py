"""Pydantic models for Guidelinely API requests and responses."""

from typing import Any, Optional, Union

from pydantic import BaseModel, model_validator

__all__ = [
    # Response models
    "GuidelineResponse",
    "CalculationResponse",
    "SourceResponse",
    "SourceDocument",
    "StatsResponse",
    "MediaResponse",
    # Request models
    "CalculateRequest",
    "BatchCalculateRequest",
    "ParameterWithUnit",
    "SearchParametersRequest",
]


class GuidelineResponse(BaseModel):
    """Single guideline result with calculated or static value.

    Represents a guideline value in PostgreSQL unitrange format (e.g., '[10 μg/L,100 μg/L]').
    """

    id: int
    parameter: str
    parameter_specification: str
    media: str
    value: str  # PostgreSQL unitrange format: '[10 μg/L,100 μg/L]', '(,87.0 μg/L]', '[5.0 mg/L,)'
    lower: Optional[float] = None  # Parsed lower bound or None if unbounded
    upper: Optional[float] = None  # Parsed upper bound or None if unbounded
    unit: str
    is_calculated: bool
    source: str
    basis: Optional[str] = None
    receptor: str
    exposure_duration: str
    guideline_type: Optional[str] = None
    notes: Optional[str] = None
    reference_id: Optional[int] = None
    document_id: Optional[int] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    document_abbreviation: str
    source_abbreviation: str


class CalculationResponse(BaseModel):
    """Response from calculation endpoints (/calculate and /calculate/batch)."""

    results: list[GuidelineResponse]
    context: dict[str, Any]  # Environmental context used for calculation
    total_count: int


class CalculateRequest(BaseModel):
    """Request body for single parameter calculation."""

    parameter: str
    media: str
    context: Optional[dict[str, str]] = None  # Environmental parameters as strings with units
    target_unit: Optional[str] = None  # Optional unit conversion


class ParameterWithUnit(BaseModel):
    """Parameter specification with optional target unit for batch requests."""

    name: str
    target_unit: Optional[str] = None


class BatchCalculateRequest(BaseModel):
    """Request body for batch parameter calculation."""

    parameters: list[Union[str, ParameterWithUnit]]  # Mix of strings and objects
    media: str
    context: Optional[dict[str, str]] = None

    @model_validator(mode="after")
    def validate_parameter_count(self) -> "BatchCalculateRequest":
        """Ensure batch doesn't exceed 50 parameters.

        This validation runs automatically when the model is instantiated,
        raising ValueError if more than 50 parameters are provided.

        Returns:
            The validated model instance.

        Raises:
            ValueError: If parameters list contains more than 50 items.
        """
        if len(self.parameters) > 50:
            raise ValueError("Maximum 50 parameters per batch request")
        return self


class SearchParametersRequest(BaseModel):
    """Request body for parameter search (optional media filter)."""

    media: Optional[list[str]] = None


class MediaResponse(BaseModel):
    """Response from /media endpoint mapping enum names to display names."""

    # Dynamic keys, so use dict directly in practice
    pass


class SourceDocument(BaseModel):
    """Nested document information within a source."""

    id: int
    title: str
    url: Optional[str] = None
    year: Optional[int] = None


class SourceResponse(BaseModel):
    """Guideline source with nested documents."""

    id: int
    name: str
    abbreviation: str
    documents: list[SourceDocument]


class StatsResponse(BaseModel):
    """Database statistics response."""

    total_parameters: int
    total_guidelines: int
    total_sources: int
    total_documents: int
