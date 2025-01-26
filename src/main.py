from spork import col, lit, Query, Dataset, Join, Entity, lag

from spork.query import Selection, Dataset, Entity, Join
import spork.window as W


def main():
    q = Query()
    selection1 = Selection(col("Thing").alias("Thang"), "JustTheName")
    selection2 = Selection(
        "AddedColumns", col("CastedColumn").cast("integer"), lit(1000).cast("timestamp")
    )
    window_selection = Selection(
        lag(col("ValidTo"), 1, lit("2024-05-25T00:21:21").cast("timestamp")).over(
            W.Window()
            .partition_by("AircraftID")
            .order_by("UpdatedUTC")
            .rows_between(W.unbounded_preceding(), W.current_row() - 1)
        )
    )

    q.select(selection1 + selection2 + window_selection)

    dataset = Dataset(
        Entity("Fully.Qualified.Ref").alias("fqr"),
        Join(
            Entity("SomeDim").alias("sd"),
            (
                col("SomeID").eq(col("SomeOtherID"))
                | ~(col("ThisAndThat") < col("SuchAndSuch"))
            ),
        ),
    )

    q = (
        q._from(dataset)
        .group_by("fqr.Thing", col("fqr.thang").cast("decimal"))
        .order_by(col("DescThis").desc())
    )
    print(q.to_string())

    """
    Output:
    select
    Thing as Thang,
    JustTheName,
    AddedColumns,
    CastedColumn::integer,
    1000::timestamp
    from Fully.Qualified.Ref fqr
    inner join SomeDim sd on ((SomeID == SomeOtherID) or NOT ((ThisAndThat < SuchAndSuch)))
    group by fqr.Thing, fqr.thang::decimal
    order by DescThis desc
    """


if __name__ == "__main__":
    main()
