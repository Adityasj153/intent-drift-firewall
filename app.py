from core.context import Context
from core.pipeline import Pipeline


def main():

    query = input("User > ")

    context = Context(query)

    pipeline = Pipeline()

    context = pipeline.run(context)

    print("\n===== PIPELINE CONTEXT =====")

    print(context.to_dict())

    if context.result is not None:

        print("\nResult")

        print(context.result)


if __name__ == "__main__":

    main()