##Association Rule Mining Program
###How the program works
Upon execution, the program:

&nbsp;&nbsp;&nbsp;&nbsp;**1:** Traverses the provided repository (or repositories) and builds file IDs for all modified files.

&nbsp;&nbsp;&nbsp;&nbsp;**2:** Then it builds 'Modified Files' data JSON file. This JSON file contains commit details, their associated
modified files, and the previously generated file IDs.

&nbsp;&nbsp;&nbsp;&nbsp;**3:** Then, the program parses the previously-created JSON file and uses the file IDs to build a transaction database.

&nbsp;&nbsp;&nbsp;&nbsp;**4:** Finally, it uses the transaction database as input for the spmf.jar file Python wrapper to work out the frequent itemsets.

###Input
The program accepts input via a CSV file, 'input_file.csv', where you specify the repository URL (repo_url), support
(min_sup), confidence, algorithm, minimum and maximum pattern length. For the sake of constraining the program's execution, you must provide minimum and maximum pattern length parameters or risk running out of Java heap space.

Note that the Apriori requires the support value (min_sup) while FP-Growth requires the support value (min_sup) and the confidence value.

The program currently supports Apriori and FP-Growth, which you can specify in each row in the input CSV file.
