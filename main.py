import streamlit as st
st.title('나의 첫 웹 서비스 만들기')
a=st.text_input('이름을 입력해주세요!')
b=st.selectbox('좋아하는 음식을 선택하세요',['치킨','마라탕','만두'])
if st.button('인사말 생성'):
  st.write(a+'님, 안녕하세요')
  st.info('반갑습니당')
  st.warning(b+'이 음식을 좋아하나봐긔?')
  st.error('요로시쿠오네가이시마스')
