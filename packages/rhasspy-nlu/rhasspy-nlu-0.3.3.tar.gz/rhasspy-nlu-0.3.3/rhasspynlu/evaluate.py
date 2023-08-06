"""Methods for evaluating recognition results."""
import logging
import typing
from dataclasses import dataclass, field

from .intent import Recognition

_LOGGER = logging.getLogger(__name__)

# -----------------------------------------------------------------------------


@dataclass
class WordError:
    """Detailed differences between reference and hypothesis strings."""

    reference: typing.List[str] = field(default_factory=list)
    hypothesis: typing.List[str] = field(default_factory=list)
    differences: typing.List[str] = field(default_factory=list)
    words: int = 0
    errors: int = 0
    matches: int = 0
    substitutions: int = 0
    deletions: int = 0
    insertions: int = 0
    error_rate: float = 0.0


@dataclass
class TestReportItem(Recognition):
    """Extended actual recognition result from TestReport."""

    expected_intent_name: str = ""
    wrong_entities: typing.List[typing.Tuple[str, str]] = field(default_factory=list)
    missing_entities: typing.List[typing.Tuple[str, str]] = field(default_factory=list)
    word_error: typing.Optional[WordError] = None


@dataclass
class TestReport:
    """Result of evaluate_intents."""

    expected: typing.Dict[str, Recognition] = field(default_factory=dict)
    actual: typing.Dict[str, TestReportItem] = field(default_factory=dict)

    # ----------
    # Statistics
    # ----------

    # Total number of WAV files
    num_wavs: int = 0

    # Number of words in all transcriptions (as counted by word_align.pl)
    num_words: int = 0

    # Total number of intents that were attempted
    num_intents: int = 0

    # Number of entity/value pairs all intents
    num_entities: int = 0

    # Number transcriptions that match *exactly*
    correct_transcriptions: int = 0

    # Number of recognized intents that match expectations
    correct_intent_names: int = 0

    # Number of correct words in all transcriptions (as computed by word_align.pl)
    correct_words: int = 0

    # Number of entity/value pairs that match *exactly* in all recognized intents
    correct_entities: int = 0

    # Number of intents where name and entities match exactly
    correct_intent_and_entities: int = 0

    transcription_accuracy: typing.Optional[float] = None

    intent_accuracy: typing.Optional[float] = None

    entity_accuracy: typing.Optional[float] = None

    intent_entity_accuracy: typing.Optional[float] = None

    # Average wav seconds / transcribe seconds
    average_transcription_speedup: typing.Optional[float] = None


# -----------------------------------------------------------------------------


def evaluate_intents(
    expected: typing.Dict[str, Recognition], actual: typing.Dict[str, Recognition]
) -> TestReport:
    """Generate report of comparison between expected and actual recognition results."""
    # Actual intents and extra info about missing entities, etc.
    report = TestReport(expected=dict(expected))

    # Real time vs transcription time
    speedups = []

    # Compute statistics
    for wav_name, actual_intent in actual.items():
        # pylint: disable=E1137
        report.actual[wav_name] = TestReportItem(**actual_intent.asdict())

        # Get corresponding expected intent
        expected_intent = expected[wav_name]

        # Compute real-time speed-up
        wav_seconds = actual_intent.wav_seconds or 0.0
        transcribe_seconds = actual_intent.transcribe_seconds or 0.0
        if (transcribe_seconds > 0) and (wav_seconds > 0):
            speedups.append(wav_seconds / transcribe_seconds)

        # Check transcriptions
        actual_text = actual_intent.raw_text or actual_intent.text
        expected_text = expected_intent.raw_text or expected_intent.text

        if expected_text == actual_text:
            report.correct_transcriptions += 1

        # Check intents
        if expected_intent.intent is not None:
            report.num_intents += 1
            if actual_intent.intent is None:
                intents_match = False
            else:
                intents_match = expected_intent.intent.name == actual_intent.intent.name

            # Count entities
            expected_entities: typing.List[typing.Tuple[str, str]] = []
            num_expected_entities = 0
            for entity in expected_intent.entities:
                report.num_entities += 1
                num_expected_entities += 1
                entity_tuple = (entity.entity, entity.value)
                expected_entities.append(entity_tuple)

            # Verify actual entities.
            # Only check entities if intent was correct.
            wrong_entities: typing.List[typing.Tuple[str, str]] = []
            missing_entities: typing.List[typing.Tuple[str, str]] = []

            if intents_match:
                report.correct_intent_names += 1
                num_actual_entities = 0
                for entity in actual_intent.entities:
                    num_actual_entities += 1
                    entity_tuple = (entity.entity, entity.value)

                    if entity_tuple in expected_entities:
                        report.correct_entities += 1
                        expected_entities.remove(entity_tuple)
                    else:
                        wrong_entities.append(entity_tuple)

                # Anything left is missing
                missing_entities = expected_entities

                # Check if entities matched *exactly*
                if (not expected_entities) and (
                    num_actual_entities == num_expected_entities
                ):
                    report.correct_intent_and_entities += 1

            # pylint: disable=E1136
            report.actual[wav_name].expected_intent_name = expected_intent.intent.name

            # pylint: disable=E1136
            report.actual[wav_name].wrong_entities = wrong_entities

            # pylint: disable=E1136
            report.actual[wav_name].missing_entities = missing_entities

        # Compute word error
        if expected_text:
            word_error = get_word_error(expected_text.split(), actual_text.split())
            report.num_words += word_error.words
            report.correct_words += word_error.words - word_error.errors

            # pylint: disable=E1136
            report.actual[wav_name].word_error = word_error

        report.num_wavs += 1

    # ---------------------------------------------------------------------

    if report.num_wavs < 1:
        _LOGGER.warning("No WAV files found")

    # Compute transcription speedup
    if speedups:
        report.average_transcription_speedup = sum(speedups) / len(speedups)

    # Summarize results
    if report.num_words > 0:
        report.transcription_accuracy = report.correct_words / report.num_words

    if report.num_intents > 0:
        report.intent_accuracy = report.correct_intent_names / report.num_intents

    if report.num_entities > 0:
        report.entity_accuracy = report.correct_entities / report.num_entities

    if report.num_intents > 0:
        report.intent_entity_accuracy = (
            report.correct_intent_and_entities / report.num_intents
        )

    return report


# -----------------------------------------------------------------------------

# Reference: https://github.com/jtsi/asr-wer


def get_word_error(
    reference: typing.List[str], hypothesis: typing.List[str]
) -> WordError:
    """Computes insertions/deletions/substituions and word error rate for two sequences of words."""
    if not reference:
        raise ValueError("Reference cannot be empty")

    reference = [w.lower() for w in reference]
    hypothesis = [w.lower() for w in hypothesis]

    if not hypothesis:
        # All error
        return WordError(
            reference=reference,
            hypothesis=hypothesis,
            differences=[w.upper() for w in hypothesis],
            insertions=len(hypothesis),
            error_rate=1,
        )

    # Initialize the matrix/table and set the first row and column equal to
    # 1, 2, 3, ...
    # Each column represent a single token in the reference string a
    # Each row represent a single token in the reference string b
    #
    rows = len(hypothesis) + 1
    cols = len(reference) + 1
    m = [[0] * cols for _ in range(rows)]

    for col in range(cols):
        for row in range(rows):
            if row == 0:
                m[0][col] = col
            elif col == 0:
                m[row][0] = row

    # Now loop over remaining cell (from the second row and column onwards)
    # The value of each selected cell is:
    #
    #   if token represented by row == token represented by column:
    #       value of the top-left diagonal cell
    #   else:
    #       calculate 3 values:
    #            * top-left diagonal cell + 1 (which represents substitution)
    #            * left cell + 1 (representing deleting)
    #            * top cell + 1 (representing insertion)
    #       value of the smallest of the three
    #
    for row in range(1, rows):
        for col in range(1, cols):
            if reference[col - 1] == hypothesis[row - 1]:
                m[row][col] = m[row - 1][col - 1]
            else:
                substitution = m[row - 1][col - 1] + 1
                insertion = m[row][col - 1] + 1
                deletion = m[row - 1][col] + 1
                m[row][col] = min(substitution, insertion, deletion)

    # and the minimum-edit distance is simply the value of the down-right most
    # cell
    errors = m[rows - 1][cols - 1]

    # Compute statistics and differences
    ref_index = len(reference)
    hyp_index = len(hypothesis)
    differences = []
    matches = 0
    substitutions = 0
    insertions = 0
    deletions = 0
    while True:
        if (ref_index <= 0) or (hyp_index <= 0):
            break

        if reference[ref_index - 1] == hypothesis[hyp_index - 1]:
            # Match
            matches += 1
            same_word = hypothesis[hyp_index - 1]
            differences.append(same_word)
            ref_index -= 1
            hyp_index -= 1
        elif m[hyp_index][ref_index] == (m[hyp_index - 1][ref_index - 1] + 1):
            # Substitution
            substitutions += 1
            ref_word = reference[ref_index - 1]
            hyp_word = hypothesis[hyp_index - 1]
            differences.append(f"{ref_word}:{hyp_word}")
            ref_index -= 1
            hyp_index -= 1
        elif m[hyp_index][ref_index] == (m[hyp_index][ref_index - 1] + 1):
            # Deletion
            deletions += 1
            ref_word = reference[ref_index - 1]
            differences.append(f"-{ref_word}")
            ref_index -= 1
        elif m[hyp_index][ref_index] == (m[hyp_index - 1][ref_index] + 1):
            # Insertion
            insertions += 1
            hyp_word = hypothesis[hyp_index - 1]
            differences.append(f"+{hyp_word}")
            hyp_index -= 1
        else:
            _LOGGER.warning("get_word_error: malformed matrix")
            break

    # error = (S + D + I) / N
    error_rate = (substitutions + deletions + insertions) / len(reference)

    return WordError(
        reference=reference,
        hypothesis=hypothesis,
        differences=list(reversed(differences)),
        words=len(reference),
        matches=matches,
        substitutions=substitutions,
        insertions=insertions,
        deletions=deletions,
        errors=errors,
        error_rate=error_rate,
    )
