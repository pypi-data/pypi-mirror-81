import importlib.util
from unittest import mock

import pandas as pd
import pytest

from great_expectations.dataset.sparkdf_dataset import SparkDFDataset


def test_sparkdfdataset_persist(spark_session):
    df = pd.DataFrame({"a": [1, 2, 3]})
    sdf = spark_session.createDataFrame(df)
    sdf.persist = mock.MagicMock()
    _ = SparkDFDataset(sdf, persist=True)
    sdf.persist.assert_called_once()

    sdf = spark_session.createDataFrame(df)
    sdf.persist = mock.MagicMock()
    _ = SparkDFDataset(sdf, persist=False)
    sdf.persist.assert_not_called()

    sdf = spark_session.createDataFrame(df)
    sdf.persist = mock.MagicMock()
    _ = SparkDFDataset(sdf)
    sdf.persist.assert_called_once()


@pytest.mark.skipif(
    importlib.util.find_spec("pyspark") is None, reason="requires the Spark library"
)
@pytest.fixture
def test_dataframe(spark_session):
    from pyspark.sql.types import IntegerType, StringType, StructField, StructType

    schema = StructType(
        [
            StructField("name", StringType(), True),
            StructField("age", IntegerType(), True),
            StructField(
                "address",
                StructType(
                    [
                        StructField("street", StringType(), True),
                        StructField("city", StringType(), True),
                        StructField("house_number", IntegerType(), True),
                    ]
                ),
                False,
            ),
            StructField("name_duplicate", StringType(), True),
            StructField("non.nested", StringType(), True),
            StructField("name_with_duplicates", StringType(), True),
            StructField("age_with_duplicates", IntegerType(), True),
            StructField(
                "address_with_duplicates",
                StructType(
                    [
                        StructField("street", StringType(), True),
                        StructField("city", StringType(), True),
                        StructField("house_number", IntegerType(), True),
                    ]
                ),
                False,
            ),
        ]
    )
    rows = [
        (
            "Alice",
            1,
            ("Street 1", "Alabama", 10),
            "Alice",
            "a",
            "Alice",
            1,
            ("Street 1", "Alabama", 12),
        ),
        (
            "Bob",
            2,
            ("Street 2", "Brooklyn", 11),
            "Bob",
            "b",
            "Bob",
            2,
            ("Street 1", "Brooklyn", 12),
        ),
        (
            "Charlie",
            3,
            ("Street 3", "Alabama", 12),
            "Charlie",
            "c",
            "Charlie",
            3,
            ("Street 1", "Alabama", 12),
        ),
        (
            "Dan",
            4,
            ("Street 4", "Boston", 12),
            "Dan",
            "d",
            "Charlie",
            3,
            ("Street 1", "Boston", 12),
        ),
    ]

    rdd = spark_session.sparkContext.parallelize(rows)

    df = spark_session.createDataFrame(rdd, schema)
    return SparkDFDataset(df, persist=True)


@pytest.mark.skipif(
    importlib.util.find_spec("pyspark") is None, reason="requires the Spark library"
)
def test_expect_column_values_to_be_of_type(spark_session, test_dataframe):
    """
    data asset expectation
    """
    from pyspark.sql.utils import AnalysisException

    assert test_dataframe.expect_column_values_to_be_of_type(
        "address.street", "StringType"
    ).success
    assert test_dataframe.expect_column_values_to_be_of_type(
        "`non.nested`", "StringType"
    ).success
    assert test_dataframe.expect_column_values_to_be_of_type(
        "name", "StringType"
    ).success
    with pytest.raises(AnalysisException):
        test_dataframe.expect_column_values_to_be_of_type("non.nested", "StringType")


@pytest.mark.skipif(
    importlib.util.find_spec("pyspark") is None, reason="requires the Spark library"
)
def test_expect_column_values_to_be_of_type(spark_session, test_dataframe):
    """
    data asset expectation
    """
    from pyspark.sql.utils import AnalysisException

    assert test_dataframe.expect_column_values_to_be_of_type(
        "address.street", "StringType"
    ).success
    assert test_dataframe.expect_column_values_to_be_of_type(
        "`non.nested`", "StringType"
    ).success
    assert test_dataframe.expect_column_values_to_be_of_type(
        "name", "StringType"
    ).success
    with pytest.raises(AnalysisException):
        test_dataframe.expect_column_values_to_be_of_type("non.nested", "StringType")


@pytest.mark.skipif(
    importlib.util.find_spec("pyspark") is None, reason="requires the Spark library"
)
def test_expect_column_values_to_be_in_type_list(spark_session, test_dataframe):
    """
    data asset expectation
    """
    from pyspark.sql.utils import AnalysisException

    assert test_dataframe.expect_column_values_to_be_in_type_list(
        "address.street", ["StringType", "IntegerType"]
    ).success
    assert test_dataframe.expect_column_values_to_be_in_type_list(
        "`non.nested`", ["StringType", "IntegerType"]
    ).success
    assert test_dataframe.expect_column_values_to_be_in_type_list(
        "name", ["StringType", "IntegerType"]
    ).success
    with pytest.raises(AnalysisException):
        test_dataframe.expect_column_values_to_be_of_type("non.nested", "StringType")


@pytest.mark.skipif(
    importlib.util.find_spec("pyspark") is None, reason="requires the Spark library"
)
def test_expect_column_pair_values_to_be_equal(spark_session, test_dataframe):
    """
    column_pair_map_expectation
    """
    from pyspark.sql.utils import AnalysisException

    assert test_dataframe.expect_column_pair_values_to_be_equal(
        "name", "name_duplicate"
    ).success
    assert not test_dataframe.expect_column_pair_values_to_be_equal(
        "name", "address.street"
    ).success
    assert not test_dataframe.expect_column_pair_values_to_be_equal(
        "name", "`non.nested`"
    ).success

    # Expectation should fail when no `` surround a non-nested column with dot notation
    with pytest.raises(AnalysisException):
        test_dataframe.expect_column_pair_values_to_be_equal("name", "non.nested")


@pytest.mark.skipif(
    importlib.util.find_spec("pyspark") is None, reason="requires the Spark library"
)
def test_expect_column_pair_values_A_to_be_greater_than_B(
    spark_session, test_dataframe
):
    """
    column_pair_map_expectation
    """
    assert test_dataframe.expect_column_pair_values_A_to_be_greater_than_B(
        "address.house_number", "age"
    ).success
    assert test_dataframe.expect_column_pair_values_A_to_be_greater_than_B(
        "age", "age", or_equal=True
    ).success


@pytest.mark.skipif(
    importlib.util.find_spec("pyspark") is None, reason="requires the Spark library"
)
def test_expect_select_column_values_to_be_unique_within_record(
    spark_session, test_dataframe
):
    """
    multicolumn_map_expectation
    """
    from pyspark.sql.utils import AnalysisException

    assert test_dataframe.expect_select_column_values_to_be_unique_within_record(
        ["name", "age"]
    ).success
    assert test_dataframe.expect_select_column_values_to_be_unique_within_record(
        ["address.street", "name"]
    ).success
    assert test_dataframe.expect_select_column_values_to_be_unique_within_record(
        ["address.street", "`non.nested`"]
    ).success

    # Expectation should fail when no `` surround a non-nested column with dot notation
    with pytest.raises(AnalysisException):
        test_dataframe.expect_select_column_values_to_be_unique_within_record(
            ["address.street", "non.nested"]
        )


@pytest.mark.skipif(
    importlib.util.find_spec("pyspark") is None, reason="requires the Spark library"
)
def test_expect_compound_columns_to_be_unique(spark_session, test_dataframe):
    """
    multicolumn_map_expectation
    """
    from pyspark.sql.utils import AnalysisException

    # Positive tests
    assert test_dataframe.expect_compound_columns_to_be_unique(["name", "age"]).success
    assert test_dataframe.expect_compound_columns_to_be_unique(
        ["address.street", "name"]
    ).success
    assert test_dataframe.expect_compound_columns_to_be_unique(
        ["address.street", "address.city"]
    ).success
    assert test_dataframe.expect_compound_columns_to_be_unique(
        ["name_with_duplicates", "age_with_duplicates", "name"]
    ).success
    assert test_dataframe.expect_compound_columns_to_be_unique(
        ["address.street", "`non.nested`"]
    ).success
    assert test_dataframe.expect_compound_columns_to_be_unique(
        ["name", "name_with_duplicates"]
    ).success
    assert test_dataframe.expect_compound_columns_to_be_unique(
        [
            "name",
            "name_with_duplicates",
            "address_with_duplicates.street",
            "address_with_duplicates.city",
            "address_with_duplicates.house_number",
        ]
    ).success

    # Negative tests
    assert not test_dataframe.expect_compound_columns_to_be_unique(
        ["address_with_duplicates.city", "address_with_duplicates.house_number"]
    ).success
    assert not test_dataframe.expect_compound_columns_to_be_unique(
        ["name_with_duplicates"]
    ).success
    assert not test_dataframe.expect_compound_columns_to_be_unique(
        ["name_with_duplicates", "address_with_duplicates.street"]
    ).success
    assert not test_dataframe.expect_compound_columns_to_be_unique(
        [
            "name_with_duplicates",
            "address_with_duplicates.street",
            "address_with_duplicates.house_number",
        ]
    ).success

    # Expectation should fail when no `` surround a non-nested column with dot notation
    with pytest.raises(AnalysisException):
        test_dataframe.expect_compound_columns_to_be_unique(
            ["address.street", "non.nested"]
        )


@pytest.mark.skipif(
    importlib.util.find_spec("pyspark") is None, reason="requires the Spark library"
)
def test_expect_column_values_to_be_unique(spark_session, test_dataframe):
    """
    column_map_expectation
    """
    from pyspark.sql.utils import AnalysisException

    assert test_dataframe.expect_column_values_to_be_unique("name").success
    assert not test_dataframe.expect_column_values_to_be_unique("address.city").success
    assert test_dataframe.expect_column_values_to_be_unique("`non.nested`").success

    # Expectation should fail when no `` surround a non-nested column with dot notation
    with pytest.raises(AnalysisException):
        test_dataframe.expect_column_values_to_be_unique("non.nested")


@pytest.mark.skipif(
    importlib.util.find_spec("pyspark") is None, reason="requires the Spark library"
)
def test_expect_column_value_lengths_to_be_between(spark_session, test_dataframe):
    """
    column_map_expectation
    """
    assert test_dataframe.expect_column_value_lengths_to_be_between(
        "name", 3, 7
    ).success
    assert test_dataframe.expect_column_value_lengths_to_be_between(
        "address.street", 1, 10
    ).success


@pytest.mark.skipif(
    importlib.util.find_spec("pyspark") is None, reason="requires the Spark library"
)
def test_expect_column_value_lengths_to_equal(spark_session, test_dataframe):
    """
    column_map_expectation
    """
    assert test_dataframe.expect_column_value_lengths_to_equal("age", 1).success
    assert test_dataframe.expect_column_value_lengths_to_equal(
        "address.street", 8
    ).success
