import sys

# Useful file reading library
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():
    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    # Here we file read using pandas
    file_reader = pd.read_csv(filename)

    # Here we numeric the months column to corresponding nums
    file_reader["Month"].replace(month_to_num, inplace=True)

    # Here we numeric visitor type as specified above
    file_reader["VisitorType"].replace({"New_Visitor": 0, "Other": 0, "Returning_Visitor": 1}, inplace=True)

    # Here we numeric weekend as specified above
    file_reader["Weekend"].replace({False: 0, True: 1}, inplace=True)

    # Here we number revenue(labels) as mentioned above
    file_reader["Revenue"].replace({False: 0, True: 1}, inplace=True)

    # Here we build a list of lists of evidence values
    evidence = []
    for index in file_reader.index:
        evidence.append(
            [int(file_reader["Administrative"][index]), float(file_reader["Administrative_Duration"][index]),
             int(file_reader["Informational"][index]), float(file_reader["Informational_Duration"][index]),
             int(file_reader["ProductRelated"][index]), float(file_reader["ProductRelated_Duration"][index]),
             float(file_reader["BounceRates"][index]), float(file_reader["ExitRates"][index]),
             float(file_reader["PageValues"][index]), float(file_reader["SpecialDay"][index]),
             int(file_reader["Month"][index]), int(file_reader["OperatingSystems"][index]),
             int(file_reader["Browser"][index]), int(file_reader["Region"][index]),
             int(file_reader["TrafficType"][index]), int(file_reader["VisitorType"][index]),
             int(file_reader["Weekend"][index])])

    # Here we build a list of label values
    labels = []
    for index in file_reader.index:
        labels.append(int(file_reader["Revenue"][index]))

    # Here we define and return our desired output
    output = (evidence, labels)
    return output


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    return KNeighborsClassifier(n_neighbors=1).fit(evidence, labels)


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    # Here we establish important values for later
    sensitivity = 0.0
    specificity = 0.0
    positive = 0.0
    negative = 0.0

    # Here we iterate through and tally values for final calc.
    for label, prediction in zip(labels, predictions):
        # Here we check for label of 1 and positive rate
        if label == 1:
            positive += 1
            if label == prediction:
                sensitivity += 1
        # Here we check for label of 0 and negativity rate
        if label == 0:
            negative += 1
            if label == prediction:
                specificity += 1

    # Here we calculate output values for sensitivity and specificity
    sensitivity /= positive
    specificity /= negative

    # Here we return desired values
    return sensitivity, specificity


# Helper dictionary to convert month names to nums
month_to_num = {"Jan": 0, "Feb": 1, "Mar": 2, "Apr": 3, "May": 4, "June": 5, "Jul": 6, "Aug": 7, "Sep": 8, "Oct": 9,
                "Nov": 10,
                "Dec": 11}

if __name__ == "__main__":
    main()
