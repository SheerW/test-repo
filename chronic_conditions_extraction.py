read_csv()


def chronic_conditions_extraction(df: pd.DataFrame, drugs_by_conditions: pd.DataFrame):
    """
    Compare pharmaceutical history with tuple of diabetes drugs to determine if member has diabetes.
    PLEASE NOTE: currently this function counts the total amount of drugs that appears in the input drug list.
    (1) It takes into account refilling (one med repeating more than once) by counting only unique occurrences of meds.
    (2) It matches case between df and drugs_by_condition. Please check how the medications are listed in member data
    before using the function and be mindful of how you interpret the results.

    parameters:
    df: pd.DataFrame
    list_diabetes_drugs: tuple
    returns:
    pd.DataFrame
    example:
    df = pd.DataFrame(data = [['person1', 'Metformin'],
                              ['person1', 'Advil'],
                              ['person2', 'Nateglinide'],
                              ['person2', 'Metformin'],
                              ['person3', 'Metformin'],
                              ['person3', 'Metformin']]
    , columns = ['member_id', 'drug_name'])
    drugs_by_conditions = pd.read_csv('drug_names_list.csv')
    df_person = count_conflicts(df, list(drug_names_list.loc[:,'diabetes']))
    df_person
      member_id  has_statins_cholesterol  has_RASA_hypertension  has_diabetes  has_liver_cirrhosis  has_thyroid_disease_drugs
    0   person1                      0.0                    0.0           1.0                  0.0                        0.0
    1   person2                      0.0                    0.0           2.0                  0.0                        0.0
    2   person3                      0.0                    0.0           2.0                  0.0                        0.0
    """
    df_split = df.groupby('member_id')
    df_person = pd.DataFrame()
    for member, member_df in df_split:
        df_person.loc[list(df_split.groups.keys()).index(member), 'member_id'] = member
        for condition_col in drugs_by_conditions.columns:
            # count the number of drugs in member_df['drug_name'] which are in drugs_by_conditions[condition_col]
            condition_member_df = member_df.loc[member_df.loc[:, 'drug_name'].isin(drugs_by_conditions[condition_col])]
            # condition_drug_count = condition_member_df.shape[0]  <-- counts total number of meds, not unique
            condition_drug_count = condition_member_df.loc[:,'drug_name'].nunique() # <-- counts only num of unique meds
            df_person.loc[list(df_split.groups.keys()).index(member), 'has_' + condition_col] = condition_drug_count
    return df_person