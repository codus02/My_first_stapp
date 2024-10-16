import streamlit as st

st.title('첫번째 웹 어플 만들기 👋')

st.write('# 1. Markdown 텍스트 작성하기')


st.markdown('''
# Markdown 문법으로 작성된 문장 출력
- 마크다운 목록1. **굵게** 표시
   - 마크다운 목록-2
      - 마크다운 목록-2-1
      - 마크다운 목록-2-2

## 마크다운 헤더2
- [네이버](https://naver.com)
- [구글](https://google.com)

### 마크다운 헤더3
일반 텍스트
''')

import pandas as pd
df = pd.DataFrame({
    '이름': ['황호동', '이순신', '강감찬'],
    '나이': [20, 45, 35]
})
st.write('## 2. DataFrame 표시하기') 
st.dataframe(df)

import numpy as np
chart_data = pd.DataFrame(np.random.rand(20, 3), columns=["a", "b", "c"])
st.write('## 3. 그래프 표시하기')
st.bar_chart(chart_data)

from PIL import Image
img = Image.open('python.png')
st.write('## 4. 이미지 표시하기')
st.image(img, width=300)
