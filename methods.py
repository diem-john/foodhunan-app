import streamlit as st


def _showrecom(ft, dm, px, cp):
    if ft == 2:
        if dm == 2:
            if px == 2:
                # 1
                if cp == 2:
                    message = 'Your location is highly recommended!'
                    st.success(message)
                # 5
                else:
                    message = 'Your business location is great, but stay competitive on providing your products or ' \
                              'services.'
                    st.success(message)
            else:
                # 4
                if cp == 2:
                    message = 'Your business location is great but consider promoting your business to increase foot ' \
                              'traffic. It can be through online platform or word of mouth.'
                    st.success(message)
                # 6
                else:
                    message = 'Your business location is good, but consider promoting your business to increase food ' \
                              'traffic and stay competitive in providing your products or services.'
                    st.info(message)
        else:
            if px == 2:
                # 3
                if cp == 2:
                    message = 'Your business location is great, but consider improving your relationship with the ' \
                              'customers to attract more of them.'
                    st.success(message)
                # 10
                else:
                    message = 'Your business location is good, but consider improving your relationship with the ' \
                              'customers to attract more of them and improve your relationship with them and stay ' \
                              'competitive on providing your products or services.'
                    st.info(message)
            else:
                # 8
                if cp == 2:
                    message = 'Your business location is good, but consider improving your relationship with the ' \
                              'customers to attract more of them and improve your relationship with them.'
                    st.info(message)
                # 12
                else:
                    message = 'Your business location is not too good. Consider improving your relationship with the ' \
                              'customers to attract more of them, stay competitive in providing your products or ' \
                              'services, and promote your business to increase food traffic and stay competitive in ' \
                              'providing your products or services.'
                    st.warning(message)
    else:
        if dm == 2:
            if px == 2:
                # 2
                if cp == 2:
                    message = 'Your business location is great but consider promoting your business to increase foot ' \
                              'traffic. It can be through online platforms or through word of mouth. '
                    st.success(message)
                # 9
                else:
                    message = 'Your business location is good, but consider promoting your business to increase foot ' \
                              'traffic. It can be through an online platform or word of mouth and stay competitive in ' \
                              'providing your products or services. '
                    st.info(message)
            else:
                # 11
                if cp == 2:
                    message = 'Your business location is good, but consider promoting your business to increase foot ' \
                              'traffic through online platform or word of mouth.'
                    st.info(message)
                # 13
                else:
                    message = 'Your business location is not too good. Consider promoting your business through an ' \
                              'online platform or word-of-mouth and stay competitive on your products and services. '
                    st.warning(message)
        else:
            if px == 2:
                # 7
                if cp == 2:
                    message = 'Your business location is good, but consider promoting your business to increase food ' \
                              'traffic and stay competitive in providing your products or services. '
                    st.info(message)
                # 14
                else:
                    message = 'Your business location is not too good. Consider promoting your business through an ' \
                              'online platform or word-of-mouth, build relationships with the customer, ' \
                              'and stay competitive on your products and services. '
                    st.warning(message)
            else:
                # 15
                if cp == 2:
                    message = 'Your business location is not too good. Consider promoting your business through the ' \
                              'online platform or word-of-mouth and building relationships with customers to attract ' \
                              'more of them. '
                    st.warning(message)
                # 16
                else:
                    message = 'Consider reviewing the location of your business to improve the business performance. ' \
                              'An online platform could be a great avenue to explore the industry. '
                    st.error(message)
    return message


def _compare(var1, var2):
    if var1 < var2:
        message = 'Excellent Financial Status'
        st.success(message)
    if var1 > var2:
        message = 'Bad Financial Status'
        st.error(message)
    if var1 == var2:
        message = 'Good Financial Status'
        st.success(message)
    return message


def _computeloanP3(r, n, p):
    return (r * p) / (1 - (1 + r) ** -n)


def _modality(modality, fa_duration):
    if modality == 12:
        dur_total = fa_duration * 1
    if modality == 4:
        dur_total = fa_duration / 3
    if modality == 1:
        dur_total = fa_duration / 12
    return dur_total


def _computeCares2(p, n):
    year = round(_toYear(n))
    if year == 1:
        return p + (p * 0.04)
    if year == 2:
        return p + (p * 0.06)
    if year == 3:
        return p + (p * 0.075)
    if year == 4:
        return p + (p * 0.08)
    else:
        return 0


def _toYear(month):
    import numpy as np
    return np.ceil(month / 12)


def _getRate(year):
    if year == 1:
        return 0.04
    if year == 2:
        return 0.06
    if year == 3:
        return 0.075
    if year == 4:
        return 0.08
    else:
        return 0
