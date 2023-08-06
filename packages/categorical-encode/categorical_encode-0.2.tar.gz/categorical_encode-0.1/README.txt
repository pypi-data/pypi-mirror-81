USAGE:

IMPORT:

from categorical_encode.categorical import categorical

The Parameters:-

:param dataframe: The Input DataFrame(X) which you want to categorically encode.
:param normalize: This parameter determines if it will be between 0-1(1 included) or 1 to no. of classes (1 - no. of classes).default:False
:param drop_columns:  This specifies the dataframe columns that need to be dropped as they are useless. default: No Columns
:param drop_na: This drops empty values (NaN) if is set to True. default: False
:param target_columns: This creates the target DataFrame(Y) without applying any Encoding. default: No Columns
:return: This Returns Two DataFrame(X,Y) if target_columns are provided Else only the Input dataframe(X) which is encoded.

Example:

from categorical_encode.categorical import categorical
df = categorical(dataframe = df, normalize= True)

This returns df as categorically encoded column wise for all the columns between 0-1(1 included).
