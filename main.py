import streamlit as st

# ==========================================
# 1. Page Configuration & Custom CSS (Warm Cream/Yellow Theme)
# ==========================================
st.set_page_config(
    page_title="MBTI 단짝 포켓몬 찾기",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom Styling using Warm Cream & Soft Yellow Palette
st.markdown("""
    <style>
    /* Global Background and Fonts */
    .stApp {
        background-color: #FFFDF0;
        font-family: 'Pretendard', 'Noto Sans KR', sans-serif;
    }
    
    /* Main Header Container */
    .main-title {
        background: linear-gradient(135deg, #FEF08A 0%, #FDE047 100%);
        padding: 2.5rem 1.5rem;
        border-radius: 24px;
        text-align: center;
        box-shadow: 0 10px 25px -5px rgba(251, 191, 36, 0.3);
        margin-bottom: 2rem;
        border: 2px solid #FCD34D;
    }
    .main-title h1 {
        color: #78350F;
        font-size: 2.3rem !important;
        font-weight: 800;
        margin-bottom: 0.5rem;
    }
    .main-title p {
        color: #92400E;
        font-size: 1.15rem;
        margin: 0;
        font-weight: 500;
    }

    /* Select Box Styling */
    .stSelectbox label {
        font-size: 1.25rem !important;
        font-weight: 700 !important;
        color: #78350F !important;
    }
    
    /* Pokemon Result Card */
    .pokemon-card {
        background-color: #FFFFFF;
        border: 3px solid #FDE047;
        border-radius: 24px;
        padding: 2rem;
        box-shadow: 0 12px 30px rgba(245, 158, 11, 0.15);
        text-align: center;
        margin-top: 1rem;
    }
    
    /* Pokemon Name & English Name */
    .pokemon-name {
        font-size: 2.2rem;
        font-weight: 800;
        color: #78350F;
        margin-bottom: 0.2rem;
    }
    .pokemon-en-name {
        font-size: 1.1rem;
        color: #D97706;
        font-weight: 600;
        margin-bottom: 1rem;
    }

    /* Type Badges */
    .type-badge {
        display: inline-block;
        background-color: #FEF3C7;
        color: #B45309;
        font-weight: 700;
        font-size: 1rem;
        padding: 0.4rem 1.2rem;
        border-radius: 50px;
        border: 1px solid #FCD34D;
        margin: 0.2rem;
    }

    /* Info Section Boxes */
    .info-box {
        background-color: #FFFBEB;
        border-left: 5px solid #F59E0B;
        border-radius: 12px;
        padding: 1.2rem;
        text-align: left;
        margin-top: 1.2rem;
    }
    .info-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: #78350F;
        margin-bottom: 0.4rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .info-text {
        font-size: 1.05rem;
        color: #451A03;
        line-height: 1.6;
        margin: 0;
    }

    /* Custom Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #F59E0B 0%, #D97706 100%);
        color: white !important;
        font-size: 1.2rem !important;
        font-weight: 700 !important;
        padding: 0.8rem 2rem !important;
        border-radius: 16px !important;
        border: none !important;
        box-shadow: 0 4px 14px rgba(217, 119, 6, 0.4) !important;
        transition: all 0.3s ease !important;
        width: 100%;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(217, 119, 6, 0.5) !important;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #B45309;
        font-size: 0.9rem;
        margin-top: 3rem;
        padding: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. Data Definition (MBTI -> Pokemon Dataset)
# ==========================================
# Official PokeAPI Artwork URLs for high quality visuals
POKEMON_DATA = {
    "ISTJ": {
        "mbti_desc": "소금형 (체계적이고 신중함)",
        "name_ko": "거북왕",
        "name_en": "Blastoise",
        "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/9.png",
        "types": ["물"],
        "traits": "묵묵하고 책임감 넘치며, 어떤 고난에도 흔들리지 않는 든든한 방어력을 가진 포켓몬.",
        "reason": "신중하고 규칙을 중요시하는 ISTJ에게 단단한 등껍질로 침착하게 자리를 지키는 거북왕은 최고의 신뢰를 주는 파트너입니다. 서로의 철저함과 책임감으로 완벽한 합을 맞출 수 있습니다."
    },
    "ISFJ": {
        "mbti_desc": "권력형 (수호자, 다정하고 헌신적)",
        "name_ko": "해피너스",
        "name_en": "Blissey",
        "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/242.png",
        "types": ["노말"],
        "traits": "상처받은 이를 정성껏 간호하고 사랑을 전하는 따뜻한 포켓몬.",
        "reason": "타인을 세심하게 배려하고 상처를 치유해주는 ISFJ의 성향은 해피너스의 온화한 마음씨와 완벽히 닮았습니다. 서로의 지친 마음을 다정하게 감싸주는 따스한 조합입니다."
    },
    "INFJ": {
        "mbti_desc": "예언자형 (통찰력 있고 이상주의적)",
        "name_ko": "가디안",
        "name_en": "Gardevoir",
        "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/282.png",
        "types": ["에스퍼", "페어리"],
        "traits": "트레이너의 마음을 예리하게 감지하며 깊은 유대감을 바탕으로 목숨 바쳐 지키는 포켓몬.",
        "reason": "깊은 감수성과 직관력을 지닌 INFJ와 정서적으로 깊게 연결될 수 있는 포켓몬입니다. 말하지 않아도 마음을 이해하고 서로를 깊이 다독여주는 운명적인 단짝이 됩니다."
    },
    "INTJ": {
        "mbti_desc": "과학자형 (전략적이고 독창적)",
        "name_ko": "후딘",
        "name_en": "Alakazam",
        "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/65.png",
        "types": ["에스퍼"],
        "traits": "IQ 5000에 달하는 엄청난 지능으로 모든 상황을 완벽하게 계산해내는 포켓몬.",
        "reason": "논리적이고 전략적인 사고를 즐기는 INTJ에게 후딘의 명석한 두뇌는 가장 뛰어난 파트너가 되어줍니다. 장기적인 계획과 지적 호기심을 공유하며 최고의 결과를 만들어냅니다."
    },
    "ISTP": {
        "mbti_desc": "백과사전형 (조용하고 냉철한 해결사)",
        "name_ko": "루카리오",
        "name_en": "Lucario",
        "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/448.png",
        "types": ["격투", "강철"],
        "traits": "파동을 감지하고 냉철한 판단으로 침착하게 상황을 해결하는 포켓몬.",
        "reason": "상황 적응력이 뛰어나고 실용적인 해결책을 찾는 ISTP에게 루카리오의 침착함과 높은 행동력은 호흡이 척척 맞습니다. 말없이도 통하는 냉철한 실전형 파트너입니다."
    },
    "ISFP": {
        "mbti_desc": "성인군자형 (온화하고 예술가적인 감성)",
        "name_ko": "이브이",
        "name_en": "Eevee",
        "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/133.png",
        "types": ["노말"],
        "traits": "다양한 가능성을 품고 자유롭게 변화하며 온화한 매력을 발산하는 포켓몬.",
        "reason": "자유로운 영혼과 따뜻한 예술가적 감성을 지닌 ISFP에게 이브이의 다채로운 가능성은 커다란 영감을 줍니다. 서로의 개성을 있는 그대로 인정해주는 편안한 사이가 됩니다."
    },
    "INFP": {
        "mbti_desc": "잔다르크형 (이상주의적이고 낭만적)",
        "name_ko": "님피아",
        "name_en": "Sylveon",
        "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/700.png",
        "types": ["페어리"],
        "traits": "리본 모양의 안테나로 다정한 파동을 보내며 적의 적의마저 가라앉히는 감성적인 포켓몬.",
        "reason": "낭만과 깊은 공감 능력을 가치 있게 여기는 INFP에게 님피아의 순수하고 다정한 에너지보다 잘 어울리는 것은 없습니다. 아름다운 동화 같은 유대를 형성할 수 있습니다."
    },
    "INTP": {
        "mbti_desc": "아이디어형 (호기심 많은 탐구가)",
        "name_ko": "폴리곤Z",
        "name_en": "Porygon-Z",
        "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/474.png",
        "types": ["노말"],
        "traits": "새로운 프로그램이 추가되어 예측 불가능하고 독특한 세계관을 가진 데이터 포켓몬.",
        "reason": "독창적이고 복잡한 독자적 생각에 몰두하는 INTP에게 폴리곤Z의 색다른 메커니즘은 호기심을 끊임없이 자극합니다. 남들과 다른 호기심을 나누는 독특한 콤비입니다."
    },
    "ESTP": {
        "mbti_desc": "수완좋은 모험가형 (스릴을 즐기는 모험가)",
        "name_ko": "윈디",
        "name_en": "Arcanine",
        "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/59.png",
        "types": ["불꽃"],
        "traits": "하루에 10,000km를 달릴 정도로 압도적인 스피드와 위엄을 가진 열정적인 포켓몬.",
        "reason": "지루함을 참지 못하고 즉각적인 스릴과 모험을 즐기는 ESTP에게 윈디의 질주력과 거침없는 에너지공급은 최고의 스릴을 선사합니다. 함께 어디든 누빌 수 있는 에너지 넘치는 단짝입니다."
    },
    "ESFP": {
        "mbti_desc": "사교적인 유형 (밝고 에너제틱한 분위기 메이커)",
        "name_ko": "피카츄",
        "name_en": "Pikachu",
        "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/25.png",
        "types": ["전기"],
        "traits": "언제나 밝고 사람을 끌어당기는 기분 좋은 에너지를 발산하는 인기 만점 포켓몬.",
        "reason": "주변을 시끌벅적하고 즐겁게 만드는 분위기 메이커 ESFP에게 피카츄의 톡톡 튀는 발랄함은 매 순간 시너지를 냅니다. 함께 있는 것만으로도 주변을 환하게 만드는 조합입니다."
    },
    "ENFP": {
        "mbti_desc": "스파크형 (열정적이고 상상력이 풍부함)",
        "name_ko": "토게키스",
        "name_en": "Togekiss",
        "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/468.png",
        "types": ["페어리", "비행"],
        "traits": "서로 인정하고 분쟁이 없는 평화로운 곳에 나타나 기쁨을 전파하는 은혜로운 포켓몬.",
        "reason": "긍정적인 에너지와 무한한 열정으로 사람들에게 행복을 전하는 ENFP에게 토게키스의 행복을 부르는 날갯짓은 완벽한 짝입니다. 만나는 모두에게 긍정의 기운을 전파합니다."
    },
    "ENTP": {
        "mbti_desc": "발명가형 (재치 있고 도전적인 토론가)",
        "name_ko": "팬텀",
        "name_en": "Gengar",
        "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/94.png",
        "types": ["고스트", "독"],
        "traits": "장난기 넘치고 신출귀몰하며 창의적인 방법으로 사람들을 깜짝 놀라게 하는 포켓몬.",
        "reason": "틀에 박힌 것을 싫어하고 장난기 넘치며 독창적인 ENTP에게 팬텀의 엉뚱함과 재치는 늘 새로운 즐거움을 줍니다. 매일이 스펙터클한 아이디어와 웃음으로 가득 찹니다."
    },
    "ESTJ": {
        "mbti_desc": "사업가형 (체계적이고 당당한 리더)",
        "name_ko": "윈디(히스이)",
        "name_en": "Dragonite",
        "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/149.png",
        "types": ["드래곤", "비행"],
        "traits": "넓은 바다를 넘나들며 난관에 처한 배를 이끌어주는 리더십과 든든한 실력을 가진 포켓몬.",
        "reason": "명확한 목표와 강한 추진력으로 조직을 이끄는 ESTJ에게 망나뇽의 압도적인 능률과 단단함은 목표를 향해 나아가는 데 더없는 지원군이 되어줍니다."
    },
    "ESFJ": {
        "mbti_desc": "친선도모형 (친절하고 협동심 강한 분위기 메이커)",
        "name_ko": "푸린",
        "name_en": "Jigglypuff",
        "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/39.png",
        "types": ["노말", "페어리"],
        "traits": "사랑스러운 노래로 사람들의 마음을 하나로 모으고 주목받기를 좋아하는 포켓몬.",
        "reason": "사람들과 어울리는 것을 좋아하고 사교성이 뛰어난 ESFJ에게 푸린의 사랑스럽고 애정 넘치는 친화력은 둘도 없는 케미를 선사합니다."
    },
    "ENFJ": {
        "mbti_desc": "언변능숙형 (카리스마와 공감 능력을 갖춘 지도자)",
        "name_ko": "리자몽",
        "name_en": "Charizard",
        "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/6.png",
        "types": ["불꽃", "비행"],
        "traits": "강한 동료애를 바탕으로 뜨거운 열정과 카리스마로 무리를 지키는 용맹한 포켓몬.",
        "reason": "타인을 이끌고 동기부여하는 ENFJ의 열정과 리자몽의 뜨거운 불꽃 에너지는 거대한 정열을 만들어냅니다. 선한 영향력과 리더십을 발휘하는 멋진 콤비입니다."
    },
    "ENTJ": {
        "mbti_desc": "지도자형 (철저한 전략가이자 결단력 있는 리더)",
        "name_ko": "마기라스",
        "name_en": "Tyranitar",
        "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/248.png",
        "types": ["바위", "악"],
        "traits": "지형마저 바꿀 정도의 압도적인 위엄과 강인한 결단력을 지닌 웅장한 포켓몬.",
        "reason": "원대한 목표를 세우고 끊임없이 도전하는 ENTJ의 야망에 마기라스의 당당하고 강력한 포스는 누구도 넘볼 수 없는 그랜드 리더십의 시너지를 발휘합니다."
    }
}

# ==========================================
# 3. Header Section UI
# ==========================================
st.markdown("""
    <div class="main-title">
        <h1>⚡ 나의 MBTI 단짝 포켓몬 찾기 ⚡</h1>
        <p>당신의 성격 유형과 딱 맞는 운명의 단짝 포켓몬을 만나보세요!</p>
    </div>
""", unsafe_allow_html=True)

# Instructions box for ease of use
st.info("💡 **사용 방법:** 아래에서 자신의 MBTI 성격 유형을 선택하고 버튼을 누르면 단짝 포켓몬이 등장합니다!")

# ==========================================
# 4. Input Section
# ==========================================
mbti_list = list(POKEMON_DATA.keys())

# Selectbox with descriptive formatting
selected_mbti = st.selectbox(
    "👉 당신의 MBTI를 선택해주세요",
    options=mbti_list,
    format_func=lambda x: f"{x} - {POKEMON_DATA[x]['mbti_desc']}"
)

# Button trigger
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    search_clicked = st.button("✨ 단짝 포켓몬 확인하기 ✨")

# ==========================================
# 5. Result Display Section
# ==========================================
if search_clicked:
    # Trigger Celebration Balloons Animation
    st.balloons()
    
    # Retrieve Data
    pokemon = POKEMON_DATA[selected_mbti]
    
    # Display Result Card
    st.markdown(f"""
        <div class="pokemon-card">
            <div style="font-size: 1.1rem; color: #B45309; font-weight: 700; margin-bottom: 0.5rem;">
                🎉 [{selected_mbti}] 유형과 운명의 짝궁! 🎉
            </div>
            <div class="pokemon-name">{pokemon['name_ko']}</div>
            <div class="pokemon-en-name">{pokemon['name_en']}</div>
        </div>
    """, unsafe_allow_html=True)

    # Centered Image Display with smooth layout
    img_col1, img_col2, img_col3 = st.columns([1, 2, 1])
    with img_col2:
        st.image(pokemon['image'], caption=f"{pokemon['name_ko']} ({pokemon['name_en']})", use_container_width=True)

    # Badges for Types
    types_html = "".join([f'<span class="type-badge">🏷️ {t} 타입</span>' for t in pokemon['types']])
    st.markdown(f'<div style="text-align: center; margin-top: 0.5rem;">{types_html}</div>', unsafe_allow_html=True)

    # Detailed Characteristics & Matching Reason
    st.markdown(f"""
        <div class="info-box">
            <div class="info-title">⭐ {pokemon['name_ko']}의 대표 특징</div>
            <p class="info-text">{pokemon['traits']}</p>
        </div>
        <div class="info-box" style="border-left-color: #D97706; background-color: #FEF3C7;">
            <div class="info-title" style="color: #92400E;">💖 단짝이 된 이유</div>
            <p class="info-text">{pokemon['reason']}</p>
        </div>
    """, unsafe_allow_html=True)

# Footer Info
st.markdown("""
    <div class="footer">
        💛 따뜻하고 즐거운 포켓몬 MBTI 단짝 탐색기 | Streamlit Cloud Ready 💛
    </div>
""", unsafe_allow_html=True)
