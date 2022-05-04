import streamlit as st
import pandas as pd
import sqlite3

conn = sqlite3.connect('data.db')
c = conn.cursor()

from datetime import date
from methods import _showrecom, _compare, _modality, _computeloanP3, _computeCares2, _toYear, _getRate

options = {'Yes': 2,
           'No': 1}

mode = {'Monthly': 12,
        'Quarterly': 4,
        'Annually': 1}


def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')


def add_userdata(username, password):
    c.execute('INSERT INTO userstable(username,password) VALUES (?,?)', (username, password))
    conn.commit()


def login_user(username, password):
    c.execute('SELECT * FROM userstable WHERE username =? AND password = ?', (username, password))
    data = c.fetchall()
    return data


st.title('Foodhunan Analyzer')
st.sidebar.title('Foodhunan Authentication:')
prompt = st.sidebar.selectbox("Options: ", ["Log-in", "Sign-up"])
if prompt == "Log-in":
    st.sidebar.subheader("Log-in Section")
    username = st.sidebar.text_input("Username:")
    password = st.sidebar.text_input("Password:", type='password')
    if st.sidebar.checkbox('Confirm Log-in'):
        create_usertable()
        login = login_user(username, password)
        if login:
            st.sidebar.success("Welcome back: {}".format(username))
            st.sidebar.header('Foodhunan Options:')
            bttn_bpt = st.sidebar.checkbox('Business Location Assessment')
            bttn_fs = st.sidebar.checkbox('Financial Assessment')
            bttn_fa = st.sidebar.checkbox('Financial Assistance (Loans)')
            bttn_sv = st.sidebar.checkbox('Save All Data')

            if bttn_bpt:
                st.header('Business Location')
                with st.form(key='analyzer'):
                    st.subheader('Foot Traffic')
                    bp1 = st.radio('There are volume of people passing by and enters my small eatery business.',
                                   list(options.keys()))
                    st.subheader('Demographics')
                    bp2 = st.radio(f"The location of my small eatery is nearby my customer's area",
                                   list(options.keys()))
                    st.subheader('Proximity')
                    bp3 = st.radio('The location of my small eatery is within the area suitable for my business.',
                                   list(options.keys()))
                    st.subheader('Competitors')
                    bp4 = st.radio(
                        'There are no other carinderias located near to the location of my small eatery business.',
                        list(options.keys()))
                    show = st.form_submit_button(label='Submit')

                ft = options[bp1]
                dm = options[bp2]
                px = options[bp3]
                cp = options[bp4]

                classification = ['Foot Traffic',
                                  'Demographics',
                                  'Proximity',
                                  'Competitors',
                                  'Result of Analyzer']
                questions = [f"There are volume of people passing by and enters my small eatery business.",
                             f"The location of my small eatery is nearby my customer's area",
                             f"The location of my small eatery is within the area suitable for my business.",
                             f"There are no other carinderias located near to the location of my small eatery business.",
                             f"Recommendation"]

                if show:
                    recomm = _showrecom(ft, dm, px, cp)
                    answers = [bp1, bp2, bp3, bp4, recomm]

                    to_df = [classification, questions, answers]

                    result = pd.DataFrame(to_df).transpose()
                    result.columns = ['Classification',
                                      'Queries',
                                      'Answers']
                    file = result.to_csv().encode('utf-8')
                    st.download_button(
                        label="Download data as CSV",
                        data=file,
                        file_name='Business_Location.csv',
                        mime='text/csv',
                    )
                    result.to_sql('businessloc_temp', conn, if_exists='replace', index=False)

            if bttn_fs:
                st.header('Financial Statement')
                with st.form(key='Analyzer_fs'):
                    capital = st.number_input('Average Capital per Month: ')
                    income = st.number_input('Average Income per Month: ')
                    submit = st.form_submit_button(label='See Result')
                if submit:
                    message = _compare(capital, income)
                    if message == 'Bad Financial Status':
                        st.info(
                            'View Financial Assistance Recommendations in Financial Assistance Tab to help you in managing your '
                            'eatery business.')
            if bttn_fa:
                with st.form(key='analyzer_fa'):
                    fa_loan = st.number_input('Desired Loan (PHP): ')
                    fa_duration = st.number_input('Desired Duration of Loan (months): ')
                    fa_mode = st.radio('Frequency of Payment: ', list(mode.keys()))
                    modality = mode[fa_mode]
                    compute = st.form_submit_button(label='Compute Loan Details')
                if compute:
                    col1, col2 = st.columns(2)
                    with col1:
                        p3_duration = fa_duration
                        p3_rate = 0.025
                        st.header("P3 Program")
                        st.subheader('P3 Calculation:')
                        if fa_loan < 5000 or fa_loan > 200000:
                            st.error('Not Eligible for P3 Program')
                            totalValueP3 = 'Not Eligible'
                            monthlyValueP3 = 'Not Eligible'
                            p3_duration = 'Not Eligible'
                            p3_rate = 'Not Eligible'
                        else:
                            totalValueP3 = round(
                                (_computeloanP3(p3_rate, _modality(modality, fa_duration), fa_loan) * _modality(
                                    modality,
                                    fa_duration)),
                                2)
                            monthlyValueP3 = round(_computeloanP3(p3_rate, _modality(modality, fa_duration), fa_loan), 2)
                            st.write('Total Loan Payment: ', totalValueP3)
                            st.write('Loan Payment Per Period: ', monthlyValueP3)
                    with col2:
                        st.header('Cares2 Program:')
                        st.subheader('Cares2 Calculation:')
                        if _computeCares2(fa_loan, fa_duration) == 0 or fa_loan < 10000 or fa_loan > 200000:
                            st.error('Not Eligible for Cares2 Program')
                            totalValueC2 = 'Not Eligible'
                            monthlyValueC2 = 'Not Eligible'
                            rate = 'Not Eligible'
                            fa_duration = 'Not Eligible'
                        else:
                            year = _toYear(fa_duration)
                            rate = _getRate(year)
                            totalValueC2 = round(_computeCares2(fa_loan, fa_duration), 2)
                            monthlyValueC2 = round(
                                (_computeCares2(fa_loan, fa_duration) / _modality(modality, fa_duration)),
                                2)
                            st.write('Total Loan Payment: ', totalValueC2)
                            st.write('Loan Payment Per Period: ', monthlyValueC2)
                        classes = ['P3 Program',
                                       'Cares2 Program']
                        interestValues = [p3_rate, rate]
                        duration = [p3_duration, fa_duration]
                        totalValues = [totalValueP3, totalValueC2]
                        monthlyValues = [monthlyValueP3, monthlyValueC2]

                        valuesTo_df = [classes, interestValues, duration, totalValues, monthlyValues]
                        values_df = pd.DataFrame(valuesTo_df).transpose()
                        values_df.columns = ['Program',
                                                 'Interest Rate/Service Charge',
                                                 'Loan Duration',
                                                 'Total Payment',
                                                 'Monthly Payment']
                        data = values_df.to_csv().encode('utf-8')
                        st.download_button(
                                label="Download data as CSV",
                                data=data,
                                file_name='Financial_Assistance.csv',
                                mime='text/csv',
                            )
                        values_df.to_sql('financialAssistance_temp', conn, if_exists='replace', index=False)
                with st.form(key='programselect'):
                    program_choice = st.radio('Select Preferred Program: ', ('P3', 'Cares2'))
                    choice = st.form_submit_button(label='Submit Choice')
                    if choice:
                        if program_choice == 'P3':
                            st.header("P3 Program")
                            st.subheader('P3 Calculation:')
                            if fa_loan < 5000 or fa_loan > 200000:
                                st.error('Not Eligible for Cares2 Program')
                            else:
                                totalValue = round(
                                    (_computeloanP3(0.025, _modality(modality, fa_duration), fa_loan) * _modality(
                                        modality,
                                        fa_duration)),
                                    2)
                                monthlyValue = round(
                                    _computeloanP3(0.025, _modality(modality, fa_duration), fa_loan),
                                    2)
                                st.write('Total Loan Value: ', totalValue)
                                st.write('Monthly Loan Value: ', monthlyValue)
                            st.subheader('About P3')
                            st.write(
                                'DTI launched the Pondo sa Pagbabago at Pag-Asenso or P3 program in 2017, starting with a PHP '
                                '1 '
                                'billion budget. The program aims to discourage underprivileged business owners from borrowing '
                                'money from loan sharks. DTI partnered with SB Corp. to provide loans to customers from the '
                                'country’s top 30 poorest provinces. More than 250 microfinancing institutions (MFIs) are '
                                'accredited by SB Corp to assist in the distribution of the P3 funds to micro-entrepreneurs. ')
                            st.subheader('Qualifications:')
                            st.write('1. Application Form')
                            st.write('2. Barangay/Municipal Business Permit')
                            st.write('3. DTI Business Name Registration (More than 50,000 of loan)')
                            st.write('4. Photocopy of Government-Issued ID')
                            st.write('5. ID Picture')
                            st.subheader('Requirements:')
                            st.write(
                                '1. Self-employed or micro-entrepreneur with a legitimate business running for at least one '
                                'year')
                            st.write('2. Valid government-issued ID')
                            st.write('3. Barangay Clearance issued in the past three months')
                            st.write('4. Proof of small enterprise activity for at least one year')
                            st.write('5. Proof of one-year residence')
                            st.write('6. ID picture')
                            st.write('7. Accomplished DTI P3 loan application form')
                            st.write('8. DTI Business Name Registration Certificate for loans over PHP 50,000')
                        if program_choice == 'Cares2':
                            st.header('Cares2 Program:')
                            st.subheader('Cares2 Calculation:')
                            if _computeCares2(fa_loan, fa_duration) == 0 or fa_loan < 10000 or fa_loan > 200000:
                                st.error(_computeCares2(fa_loan, fa_duration))
                                st.error('Not Eligible for Cares2 Program')
                            else:
                                totalValue = round(_computeCares2(fa_loan, fa_duration), 2)
                                monthlyValue = round(
                                    (_computeCares2(fa_loan, fa_duration) / _modality(modality, fa_duration)),
                                    2)
                                st.write('Total Loan Value: ', totalValue)
                                st.write('Monthly Loan Value: ', monthlyValue)
                            st.subheader('About Cares2')
                            st.write(
                                'The CARES Program is a Php 1 billion Enterprise Rehabilitation Financing (ERF) loan '
                                'facility '
                                'under the P3 Program. MSMEs can avail of interest-free loans, helping them recover '
                                'from the '
                                'economic impact of the pandemic.Through this government loan for small businesses, '
                                'micro-enterprises with an asset size of not more than Php 3 million can borrow Php 10,'
                                '000 up to Php 200,000. Meanwhile, small enterprises with an asset size of not more '
                                'than Php 15 '
                                'million can borrow a higher loan amount up to Php 500,000.')
                            st.subheader('Qualifications')
                            st.write('1. Make sure the business is 100% Filipino-owned')
                            st.write('2. Must be in operation for at least a year before March 16, 2020')
                            st.write(
                                '3. Assets should not be over PHP 15 million, excluding the land where the business '
                                'office or '
                                'facility is located')
                            st.write(
                                '4. Affected by the ECQ in Luzon or similar community quarantine areas in Visayas and '
                                'Mindanao')
                            st.subheader('Requirements')
                            st.write('1. Accomplished loan application form and signature card')
                            st.write('2. Valid government-issued ID with photo')
                            st.write('3. Barangay certification of business')
                            st.write('4. Proof of permanent business address')
                        st.subheader('Contact Details:')
                        st.write('For more information about these loans, you may reach out to Small Business '
                                 'Corporation contact details:  (632) 8 651-3333 or email '
                                 'cares@sbgfc.org.ph/sbcorporation@sbgfc.org.ph')
                        st.write('Cellphone Numbers:')
                        st.write('Central Luzon (Smart: 0928.768.4674 / Globe: 0956.688.9496)')
                        st.write('North Luzon (Smart: 0949.712.0802 / Globe: 0956.688.9518)')
                        st.write('Visayas (Smart: 0921.534.3584 / Globe: 0995.549.2889)')
                        st.write('Mindanao (Smart: 0949.712.0780 / Globe: 0956.674.0639)')
                        st.write('Company Address: ')
                        st.write(
                            '17th & 18th Floors, 139 Corporate Center, Valero St., Salcedo Village, Makati City '
                            '1227 Philippines')
            if bttn_sv:
                try:
                    query1 = 'SELECT * from businessloc_temp'
                    result = pd.read_sql_query(query1, conn)
                    st.dataframe(result)
                    file = result.to_csv().encode('utf-8')
                    st.download_button(
                        label="Download data as CSV",
                        data=file,
                        file_name='Business_Location.csv',
                        mime='text/csv',
                    )
                except:
                    st.error('No input at Business Location tab to proceed')
                try:
                    query2 = 'SELECT * from financialAssistance_temp'
                    values_df = pd.read_sql_query(query2, conn)
                    st.dataframe(values_df)
                    data = values_df.to_csv().encode('utf-8')
                    st.download_button(
                        label="Download data as CSV",
                        data=data,
                        file_name='Financial_Assistance.csv',
                        mime='text/csv',
                    )
                except:
                    st.error('No input at Financial Assistance tab to proceed')

        else:
            st.sidebar.error('Invalid username/password')

if prompt == "Sign-up":
    st.sidebar.subheader("Sign-up")
    new_user = st.sidebar.text_input('Username:')
    new_password = st.sidebar.text_input('Password', type='password')
    if st.sidebar.checkbox('Read Terms and Agreement'):
        st.write('Please read these terms and conditions carefully before using Foodhunan application operated by '
                 'Joshua Cruz and Alliah Makinano.')
        st.subheader('Conditions of Use')
        st.write('By using this website, you certify that you have read and reviewed this Agreement and that you '
                 'agree to comply with its terms. If you do not want to be bound by the terms of this Agreement, '
                 'you are advised to leave the website accordingly. Foodhunan only grants use and access of this '
                 'website, its products, and its services to those who have accepted its terms.')
        st.subheader('Privacy Policy')
        st.write('Before you continue using our mobile application, we advise you to read our terms and conditions '
                 'regarding the user data collection. It will help you better understand our practices.')
        st.subheader('Age Restriction')
        st.write('You must be at least 18 (eighteen) years of age before you can use this mobile application. By '
                 'using this mobile application, you warrant that you are at least 18 years of age and you may '
                 'legally adhere to this Agreement. Foodhunan assumes no responsibility for liabilities related to '
                 'age misrepresentation.')
        st.subheader('Intellectual Property')
        st.write('You agree that all materials, products, and services provided on this website are the property of '
                 'Foodhunan , its affiliates, directors, officers, employees, agents, suppliers, or licensors '
                 'including all copyrights, trade secrets, trademarks, patents, and other intellectual property. You '
                 'also agree that you will not reproduce or redistribute the Foodhunan’s intellectual property in any '
                 'way, including electronic, digital, or new trademark registrations.')
        st.subheader('User Accounts')
        st.write('As a user of this website, you may be asked to register with us and provide private information. '
                 'You are responsible for ensuring the accuracy of this information, and you are responsible for '
                 'maintaining the safety and security of your identifying information. You are also responsible for '
                 'all activities that occur under your account or password.')
        st.write('If you think there are any possible issues regarding the security of your account on the website, '
                 'inform us immediately so we may address them accordingly.')
        st.write('We reserve all rights to terminate accounts, edit or remove content and cancel orders at our sole '
                 'discretion.')
        st.subheader('Applicable Law')
        st.write('By visiting this website, you agree that the laws of the Philippines, without regard to principles '
                 'of conflict laws, will govern these terms and conditions, or any dispute of any sort that might '
                 'come between Foodhunan and you, or its business partners and associates.')
        st.subheader('Disputes')
        st.write('Any dispute related in any way to your visit to this website or to products you purchase from us '
                 'shall be arbitrated by state or federal court Philippines and you consent to exclusive jurisdiction '
                 'and venue of such courts.')
        st.subheader('Imdemnification')
        st.write('You agree to indemnify Foodhunan and its affiliates and hold Foodhunan harmless against legal '
                 'claims and demands that may arise from your use or misuse of our services. We reserve the right to '
                 'select our own legal counsel.')
        st.subheader('Limitation on Liability')
        st.write('Foodhunan is not liable for any damages that may occur to you as a result of your misuse of our '
                 'website.')
        st.write('Foodhunan reserves the right to edit, modify, and change this Agreement at any time. We shall let '
                 'our users know of these changes through electronic mail. This Agreement is an understanding between '
                 'Foodhunan and the user, and this supersedes and replaces all prior agreements regarding the use of '
                 'this website.')
        if st.checkbox('I agree to the terms and conditions'):
            if st.sidebar.button("Sign-up"):
                create_usertable()
                add_userdata(new_user, new_password)
                st.sidebar.success("You have successfully created a foodhunan account!")
                st.sidebar.info('Proceed to Log-in')
