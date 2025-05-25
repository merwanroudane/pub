import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
# import altair as alt # Not used in the final version
# from streamlit_echarts import st_echarts # Not used in the final version
import arabic_reshaper
from bidi.algorithm import get_display

# ضبط إعدادات الصفحة
st.set_page_config(
	page_title="دليل التعامل مع رفض المقالات العلمية الاقتصادية",
	page_icon="📊",
	layout="wide",
	initial_sidebar_state="expanded"
)

# إضافة CSS للتنسيق
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Almarai:wght@300;400;700&display=swap');

    * {
        font-family: 'Almarai', sans-serif;
    }

    body {
        direction: rtl; /* Set base direction for the whole page */
    }

    h1, h2, h3, h4, h5, h6 {
        text-align: right;
        color: #1e3d59; /* Dark Blue */
    }

    .main { /* Default Streamlit main container */
        text-align: right;
        direction: rtl;
    }

    div[data-testid="stBlock"], div[data-testid="stVerticalBlock"] {
        text-align: right;
        direction: rtl;
    }

    div[data-testid="stSidebar"] * {
        text-align: right;
        direction: rtl;
    }

    div[data-testid="stSidebarNav"] ul {
        padding-right: 0px; 
    }

    div[data-testid="stSidebarNav"] li {
        padding-right: 10px; 
    }

    .stRadio > label, .stSelectbox > label, .stTextInput > label, .stTextArea > label {
        text-align: right !important;
        direction: rtl !important;
        display: block; /* Ensure label takes full width for alignment */
    }

    div.row-widget.stRadio > div {
        flex-direction: row-reverse;
        justify-content: flex-end; 
    }

    .stTabs [data-baseweb="tab-list"] {
        direction: rtl;
    }

    .stTabs [data-baseweb="tab"] {
        direction: rtl;
        text-align: right;
        padding-right: 10px;
        padding-left: 10px;
    }

    p, li, div.stMarkdown div { 
        text-align: right;
        direction: rtl;
    }

    /* Custom Boxes */
    .info-box {
        background-color: #e7f3fe; 
        border-radius: 10px;
        padding: 20px;
        margin: 15px 0;
        border-right: 5px solid #0366d6; 
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }

    .warning-box {
        background-color: #fff8f1; 
        border-radius: 10px;
        padding: 20px;
        margin: 15px 0;
        border-right: 5px solid #d66a03; 
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }

    .success-box {
        background-color: #f1fff8; 
        border-radius: 10px;
        padding: 20px;
        margin: 15px 0;
        border-right: 5px solid #03d67a; 
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }

    .tip-box {
        background-color: #f5f0ff; 
        border-radius: 10px;
        padding: 20px;
        margin: 15px 0;
        border-right: 5px solid #6e03d6; 
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }

    .big-number {
        font-size: 3rem; 
        font-weight: bold;
        color: #1e3d59; 
        text-align: center;
        padding-top: 10px;
    }

    .card {
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); 
        transition: transform 0.2s;
    }
    .card:hover {
        transform: translateY(-5px);
    }

    .highlight {
        background-color: #ffffcc; 
        padding: 2px 5px;
        border-radius: 4px;
        font-weight: bold;
    }

    .step-box {
        background-color: #f9f9f9; 
        border-radius: 10px;
        padding: 20px;
        margin: 15px 0;
        border-right: 5px solid #555; 
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }

    .step-number {
        background-color: #1e3d59; 
        color: white;
        width: 35px; 
        height: 35px; 
        border-radius: 50%;
        display: inline-flex;
        justify-content: center;
        align-items: center;
        margin-left: 15px; 
        font-weight: bold;
        font-size: 1.1rem;
    }

    .example-box {
        background-color: #ffffff;
        border: 1px solid #e0e0e0; 
        border-radius: 8px;
        padding: 15px;
        margin: 15px 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }

    /* Ensure Plotly chart titles are right-aligned */
    .js-plotly-plot .plotly .g-gtitle {
        text-anchor: end !important;
    }
    /* Fix for Streamlit dataframe header alignment with RTL */
    .stDataFrame table th {
        text-align: right !important;
        direction: rtl !important;
    }
    .stDataFrame table td {
        text-align: right !important; /* Or 'inherit' if cells have mixed content */
        direction: rtl !important;
    }
</style>
""", unsafe_allow_html=True)


# تعريف الوظائف المساعدة
def plot_arabic_pie_plotly(data_values, data_labels_raw, title_text_raw, values_col_name, labels_col_name):
	"""
	Generates a Plotly pie chart with Arabic text support.
	It's often better to pass raw Arabic strings to Plotly and let it handle rendering with a suitable font.
	If Plotly misrenders, then uncomment the reshaping/bidi lines.
	"""
	custom_colors = ['#ff6b6b', '#4ecdc4', '#1a535c', '#ff9f1c', '#2ec4b6', '#e71d36', '#662e9b', '#43aa8b', '#fca311',
					 '#9e2a2b']

	# Option 1: Pass raw strings (preferred if Plotly handles it)
	processed_labels = [str(label) for label in data_labels_raw]
	processed_title = str(title_text_raw)
	legend_title = "الأسباب"

	# Option 2: If Plotly misrenders raw strings, uncomment these lines
	# processed_labels = [get_display(arabic_reshaper.reshape(str(label))) for label in data_labels_raw]
	# processed_title = get_display(arabic_reshaper.reshape(str(title_text_raw)))
	# legend_title = get_display(arabic_reshaper.reshape("الأسباب"))

	df_chart = pd.DataFrame({
		labels_col_name: processed_labels,
		values_col_name: data_values
	})

	fig = px.pie(df_chart,
				 values=values_col_name,
				 names=labels_col_name,
				 title=processed_title,
				 color_discrete_sequence=custom_colors[:len(data_values)])

	fig.update_traces(textposition='inside',
					  textinfo='percent+label',
					  insidetextorientation='radial',
					  hoverinfo='label+percent+value',
					  textfont_size=12,
					  marker=dict(line=dict(color='#FFFFFF', width=2)))

	fig.update_layout(
		title_font_size=18,
		title_x=0.5,
		title_y=0.95,
		title_xanchor='center',
		title_yanchor='top',
		font_family="Almarai, sans-serif",  # Ensure Plotly uses the Arabic font
		legend_title_text=legend_title,
		legend=dict(
			orientation="h",
			yanchor="bottom",
			y=-0.2,
			xanchor="center",
			x=0.5,
			traceorder="normal",
			font=dict(
				family="Almarai, sans-serif",
				size=10,
				color="black"
			),
			title_font_family="Almarai, sans-serif"
		),
		margin=dict(t=60, b=100, l=20, r=20)
	)
	return fig


# البيانات (تبقى كما هي)
reasons_data = {
	'سبب الرفض': [
		'منهجية البحث ضعيفة',
		'نتائج غير مقنعة أو غير مدعومة',
		'ملاءمة الموضوع للمجلة',
		'جودة الكتابة والتحرير',
		'مراجعة أدبيات غير كافية',
		'أصالة البحث ومساهمته',
		'إشكالية في تصميم البحث',
		'أخطاء إحصائية أو تحليلية'
	],
	'النسبة المئوية': [28, 23, 15, 12, 9, 8, 3, 2]
}

rejection_types = {
	'نوع الرفض': [
		'رفض مباشر (Desk Rejection)',
		'رفض بعد التحكيم (Rejection after Review)',
		'رفض مع إمكانية إعادة التقديم (Reject and Resubmit)',
		'رفض مع التشجيع على التقديم لمجلة أخرى'
	],
	'الوصف': [
		'يتم من قبل المحرر دون إرسال للتحكيم، عادة بسبب عدم الملاءمة أو ضعف واضح',
		'يتم بعد تقييم المحكمين للبحث، بسبب مشاكل منهجية أو أخطاء جوهرية',
		'رفض البحث بصيغته الحالية مع السماح بإعادة تقديمه بعد تعديلات جذرية',
		'رفض مع اقتراح مجلات بديلة أكثر ملاءمة للبحث'
	],
	'النسبة المئوية': [40, 35, 15, 10]
}

reviewers_comments = {
	'نوع التعليق': [
		'تعليقات منهجية',
		'تعليقات على النتائج والتحليل',
		'تعليقات على الأدبيات',
		'تعليقات لغوية وتحريرية',
		'تعليقات على الأصالة والمساهمة',
		'تعليقات على البيانات'
	],
	'الأمثلة': [
		'العينة المستخدمة غير ممثلة للمجتمع المستهدف • منهجية البحث غير موضحة بشكل كاف • هناك مشاكل في تصميم الاستبيان',
		'النتائج لا تدعم الاستنتاجات • الإحصاءات الوصفية غير كافية • هناك حاجة لاختبارات إحصائية إضافية',
		'المراجعة الأدبية غير محدثة • لم يتم الإشارة إلى دراسات مهمة في المجال • ضعف الربط بين الدراسات السابقة وموضوع البحث',
		'لغة البحث ضعيفة وتحتاج تحرير لغوي • عدم وضوح العرض • مشاكل في التنسيق وهيكل البحث',
		'المساهمة العلمية للبحث غير واضحة • الموضوع مكرر وتم بحثه سابقاً • لا يضيف جديداً للمعرفة في المجال',
		'البيانات غير كافية • مصادر البيانات غير موثوقة • طريقة جمع البيانات غير مناسبة'
	],
	'النسبة المئوية': [30, 25, 15, 12, 10, 8]
}

responses_data = {
	'نوع التعامل': [
		'رد علمي مدعم بالأدلة',
		'قبول التعليق مع تعديل',
		'توضيح سوء فهم',
		'تقديم تحليل إضافي',
		'الاعتراف بالقيود'
	],
	'النسبة المئوية': [35, 30, 20, 10, 5]
}


# الصفحة الرئيسية
def main_page():
	st.title("دليل التعامل مع رفض المقالات العلمية في المجلات الاقتصادية")  # Raw Arabic

	st.markdown("""
    <div class="info-box">
        <h3>مرحباً بك في هذا الدليل الشامل!</h3>
        <p>يهدف هذا الدليل إلى تزويد الباحثين في مجال الاقتصاد بالأدوات والمعرفة اللازمة لفهم أسباب رفض المقالات العلمية وكيفية التعامل معها بفعالية. 
        النشر العلمي عملية تنافسية، والرفض جزء طبيعي منها. هذا التطبيق يقدم تحليلات لقرارات المحكمين، استراتيجيات للرد والتعديل، ونصائح عملية لزيادة فرص قبول بحثك في المجلات المرموقة.</p>
        <h4>لماذا هذا الدليل؟</h4>
        <ul>
            <li><strong>فهم التحديات:</strong> التعرف على الأسباب الشائعة للرفض لتجنبها مستقبلاً.</li>
            <li><strong>تحويل الرفض إلى فرصة:</strong> استخدام تعليقات المحكمين كأداة لتطوير البحث وتعزيز جودته.</li>
            <li><strong>تعزيز مهارات النشر:</strong> اكتساب استراتيجيات فعالة للرد على المحكمين وإعادة تقديم الأبحاث.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)  # HTML within markdown uses CSS for RTL

	st.markdown("## لمحة سريعة عن واقع النشر العلمي")  # Raw Arabic
	col1, col2, col3 = st.columns(3)

	with col1:
		st.markdown("""
        <div class="card" style="background-color: #f0f7ff;">
            <div class="big-number">~70-90%</div>
            <p style="text-align: center;">نسبة الرفض في المجلات الاقتصادية عالية التأثير (Q1/Q2)</p>
        </div>
        """, unsafe_allow_html=True)

	with col2:
		st.markdown("""
        <div class="card" style="background-color: #fff0f0;">
            <div class="big-number">2-4</div>
            <p style="text-align: center;">متوسط عدد المحكمين الذين يراجعون البحث الواحد</p>
        </div>
        """, unsafe_allow_html=True)

	with col3:
		st.markdown("""
        <div class="card" style="background-color: #f0fff5;">
            <div class="big-number">~50%</div>
            <p style="text-align: center;">من الأبحاث المرفوضة تُنشر لاحقاً بعد التعديلات المناسبة</p>
        </div>
        """, unsafe_allow_html=True)

	st.markdown("## كيف تستخدم هذا الدليل؟")  # Raw Arabic
	st.markdown("""
    <div class="tip-box">
        <p>استخدم الشريط الجانبي للتنقل بين أقسام الدليل المختلفة. كل قسم يركز على جانب محدد من عملية التعامل مع رفض المقالات:</p>
        <ul>
            <li><strong>أسباب رفض المقالات:</strong> لفهم المشاكل الشائعة التي تؤدي للرفض.</li>
            <li><strong>أنواع قرارات الرفض:</strong> للتعرف على دلالات كل قرار وكيفية التعامل معه.</li>
            <li><strong>تحليل تعليقات المحكمين:</strong> لفك شفرة ملاحظات المراجعين وتحديد أولويات الرد.</li>
            <li><strong>استراتيجيات الرد والتعديل:</strong> لتعلم كيفية صياغة ردود فعالة وإجراء التعديلات اللازمة.</li>
            <li><strong>الأسئلة الشائعة:</strong> للحصول على إجابات سريعة لأكثر الاستفسارات تكراراً.</li>
        </ul>
        <p>نأمل أن يكون هذا الدليل عوناً لك في رحلتك البحثية.</p>
    </div>
    """, unsafe_allow_html=True)

	st.markdown("## محتويات الدليل التفصيلية")  # Raw Arabic

	col1_content, col2_content = st.columns(2)

	with col1_content:
		st.markdown("""
        <div style="background-color: #f5f5f5; padding: 15px; border-radius: 10px; margin-bottom: 10px;">
            <h4>📊 أسباب رفض المقالات الاقتصادية</h4>
            <ul>
                <li>تحليل الأسباب الرئيسية للرفض مع نسب مئوية.</li>
                <li>أمثلة واقعية من تعليقات المحكمين.</li>
                <li>حلول مقترحة لتجنب نقاط الضعف الشائعة.</li>
            </ul>
        </div>

        <div style="background-color: #f5f5f5; padding: 15px; border-radius: 10px; margin-bottom: 10px;">
            <h4>📝 أنواع قرارات الرفض</h4>
            <ul>
                <li>شرح مفصل لرفض مباشر (Desk Rejection)، رفض بعد التحكيم، ورفض مع إمكانية إعادة التقديم.</li>
                <li>خصائص كل نوع وكيفية التعامل الأمثل معه.</li>
                <li>أمثلة لرسائل الرفض المختلفة.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

	with col2_content:
		st.markdown("""
        <div style="background-color: #f5f5f5; padding: 15px; border-radius: 10px; margin-bottom: 10px;">
            <h4>🔍 تحليل تعليقات المحكمين</h4>
            <ul>
                <li>تصنيف أنواع التعليقات الشائعة ونسبتها.</li>
                <li>استراتيجيات لفهم وتحليل ملاحظات المحكمين.</li>
                <li>نصائح للتعامل مع التعليقات المتناقضة أو الصعبة.</li>
                <li>أداة تفاعلية لتصنيف التعليقات.</li>
            </ul>
        </div>

        <div style="background-color: #f5f5f5; padding: 15px; border-radius: 10px; margin-bottom: 10px;">
            <h4>✅ استراتيجيات الرد والتعديل</h4>
            <ul>
                <li>مبادئ أساسية لصياغة ردود فعالة ومهنية.</li>
                <li>هيكل نموذجي لرسالة الرد على المحكمين.</li>
                <li>أمثلة لأنواع مختلفة من الردود (قبول، توضيح، رفض مبرر).</li>
                <li>نصائح لتجنب الأخطاء الشائعة في الرد.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

	st.markdown("---")

	st.markdown("""
    <div class="success-box">
        <h3>تذكر دائماً: الرفض ليس النهاية!</h3>
        <p>لا تتعامل مع رفض البحث بشكل شخصي. اعتبره فرصة قيمة لتطوير بحثك، صقل مهاراتك الأكاديمية، وزيادة فهمك لمتطلبات النشر العلمي عالي الجودة. 
        العديد من الأبحاث المرموقة مرت بمراحل رفض ومراجعات متعددة قبل أن ترى النور. المثابرة والتعلم من التجربة هما مفتاح النجاح.</p>
    </div>
    """, unsafe_allow_html=True)


# صفحة أسباب الرفض
def rejection_reasons_page():
	st.title("أسباب رفض المقالات في المجلات الاقتصادية")

	st.markdown("""
    <div class="info-box">
        <p>فهم الأسباب الشائعة لرفض المقالات العلمية في المجلات الاقتصادية هو الخطوة الأولى لتجنب الوقوع في نفس الأخطاء.
        تختلف هذه الأسباب في أهميتها وتأثيرها، لكن معرفتها تساعد الباحثين على تحسين جودة أبحاثهم قبل التقديم.</p>
    </div>
    """, unsafe_allow_html=True)

	st.subheader("الأسباب الرئيسية للرفض ونسبتها")
	df_reasons = pd.DataFrame(reasons_data)
	fig_reasons = plot_arabic_pie_plotly(
		df_reasons['النسبة المئوية'],
		df_reasons['سبب الرفض'],  # Pass raw Arabic labels
		"توزيع أسباب رفض المقالات الاقتصادية",  # Pass raw Arabic title
		'النسبة المئوية',
		'سبب الرفض'
	)
	st.plotly_chart(fig_reasons, use_container_width=True)

	st.subheader("شرح تفصيلي لأسباب الرفض")

	with st.expander("منهجية البحث ضعيفة (28%)"):  # Raw Arabic
		st.markdown("""
        <div class="step-box">
            <h4>المشكلة:</h4>
            <p>تعتبر المنهجية الضعيفة من أكثر أسباب رفض البحوث شيوعاً. قد تشمل المشاكل:</p>
            <ul>
                <li>عدم وضوح المنهجية المستخدمة أو عدم تبريرها بشكل كافٍ</li>
                <li>عينة غير ممثلة أو حجم عينة غير كافٍ (مثلاً، N &lt; 30 لدراسة كمية معقدة)</li>
                <li>أخطاء في تصميم الدراسة أو جمع البيانات</li>
                <li>منهجية لا تتناسب مع أسئلة البحث</li>
                <li>عدم معالجة القيود المنهجية المحتملة</li>
            </ul>

            <h4>أمثلة من تعليقات المحكمين:</h4>
            <div class="example-box">
                <p>"المنهجية المستخدمة غير واضحة وتفتقر للتفاصيل الكافية لإعادة إنتاج الدراسة."</p>
                <p>"حجم العينة صغير جداً (N=32) ولا يسمح بتعميم النتائج كما يدعي الباحثون."</p>
                <p>"الأدوات المستخدمة في القياس لم تخضع للتحقق من صدقها وثباتها في سياق الدراسة الحالية."</p>
            </div>

            <h4>الحلول:</h4>
            <ol>
                <li>وصف المنهجية بشكل تفصيلي ودقيق، مع تبرير واضح لكل خيار منهجي</li>
                <li>التأكد من كفاية حجم العينة وتمثيلها للمجتمع المستهدف (استخدم تحليل القوة الإحصائية)</li>
                <li>استشارة خبراء إحصائيين لمراجعة التصميم البحثي</li>
                <li>اختبار المنهجية بدراسة تجريبية صغيرة قبل التنفيذ الكامل</li>
                <li>مراجعة الأدبيات المنهجية الحديثة في مجالك للتعرف على أفضل الممارسات</li>
                <li>مناقشة قيود المنهجية بشكل صريح في البحث</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)

	with st.expander("نتائج غير مقنعة أو غير مدعومة (23%)"):  # Raw Arabic
		st.markdown("""
        <div class="step-box">
            <h4>المشكلة:</h4>
            <p>قد تكون النتائج ضعيفة أو غير مدعومة بشكل كافٍ بالبيانات، أو قد تكون هناك مشاكل في عرض وتفسير النتائج:</p>
            <ul>
                <li>تعميمات مبالغ فيها تتجاوز ما تدعمه البيانات</li>
                <li>عدم اتساق بين النتائج والاستنتاجات</li>
                <li>نقص في التحليلات الإحصائية الداعمة</li>
                <li>عدم معالجة النتائج المتضاربة أو غير المتوقعة</li>
                <li>عرض انتقائي للنتائج (Cherry-picking)</li>
            </ul>

            <h4>أمثلة من تعليقات المحكمين:</h4>
            <div class="example-box">
                <p>"الاستنتاجات التي توصل إليها الباحثون أوسع بكثير مما تدعمه البيانات المقدمة."</p>
                <p>"هناك تناقض بين النتائج الكمية في الجدول 3 والتفسيرات النوعية في القسم 4.2."</p>
                <p>"الدراسة تفتقر إلى اختبارات إحصائية كافية للتحقق من صحة الفرضيات المطروحة، مثل اختبارات المتانة (robustness checks)."</p>
            </div>

            <h4>الحلول:</h4>
            <ol>
                <li>تقديم تحليلات إحصائية شاملة وملائمة لنوع البيانات وأسئلة البحث</li>
                <li>عرض النتائج بشكل موضوعي ودقيق، دون مبالغة في الاستنتاجات</li>
                <li>مناقشة النتائج غير المتوقعة أو المتضاربة بدلاً من تجاهلها، وحاول تفسيرها</li>
                <li>استخدام الرسوم البيانية والجداول بشكل فعال لتوضيح النتائج (مع تسميات واضحة)</li>
                <li>ربط النتائج بالأدبيات السابقة لتقوية تفسيراتك وإظهار مساهمة بحثك</li>
                <li>التمييز بوضوح بين النتائج (ما وجدته) والتفسيرات (ماذا يعني) والتوصيات (ماذا يجب فعله)</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
	# ... (Repeat for all expanders, using raw Arabic strings for titles) ...
	with st.expander("ملاءمة الموضوع للمجلة (15%)"):
		st.markdown("""
        <div class="step-box">
            <h4>المشكلة:</h4>
            <p>عدم توافق موضوع البحث مع نطاق المجلة واهتماماتها:</p>
            <ul>
                <li>موضوع البحث خارج نطاق اهتمام المجلة (Aims & Scope)</li>
                <li>عدم التوافق مع الجمهور المستهدف للمجلة</li>
                <li>استخدام منهجيات غير مألوفة أو غير مقبولة في المجلة</li>
                <li>عدم الإشارة للأبحاث المنشورة سابقاً في المجلة (يظهر عدم اطلاع على المجلة)</li>
                <li>مستوى البحث (نظري جداً أو تطبيقي جداً) لا يناسب توجه المجلة</li>
            </ul>
            <h4>أمثلة من تعليقات المحكمين:</h4>
            <div class="example-box">
                <p>"على الرغم من جودة البحث، إلا أن موضوعه يقع خارج نطاق اهتمام مجلتنا المتخصصة في الاقتصاد الكلي، بينما يركز البحث على قضايا الاقتصاد الجزئي السلوكي."</p>
                <p>"هذه الدراسة تركز على الجوانب السلوكية أكثر من التحليل الاقتصادي الذي تهتم به المجلة."</p>
                <p>"لم يتم الإشارة إلى الأدبيات ذات الصلة المنشورة في مجلتنا خلال السنوات الثلاث الأخيرة، مما يجعل من الصعب تقييم مدى ملاءمة البحث لتوجهات المجلة."</p>
            </div>
            <h4>الحلول:</h4>
            <ol>
                <li>دراسة نطاق المجلة بعناية قبل التقديم (اقرأ بيان المهمة والأهداف Aims and Scope)</li>
                <li>مراجعة الأعداد الأخيرة من المجلة لفهم أنواع البحوث التي تنشرها وأحدث توجهاتها</li>
                <li>الإشارة بوضوح في المقدمة وخطاب التقديم (Cover Letter) إلى كيفية ارتباط بحثك بمجال اهتمام المجلة</li>
                <li>الاستشهاد بالأبحاث ذات الصلة المنشورة في المجلة نفسها، إن وجدت وصلة حقيقية</li>
                <li>التواصل مع المحرر (Pre-submission inquiry) قبل التقديم إذا كنت غير متأكد من ملاءمة البحث</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)

	with st.expander("جودة الكتابة والتحرير (12%)"):
		st.markdown("""
        <div class="step-box">
            <h4>المشكلة:</h4>
            <p>ضعف في الكتابة العلمية أو مشاكل في التنظيم والتحرير:</p>
            <ul>
                <li>أخطاء لغوية ونحوية وإملائية متكررة</li>
                <li>عدم وضوح في العرض وتنظيم الأفكار، وترابط ضعيف بين الفقرات</li>
                <li>هيكل غير منطقي أو متماسك للبحث (تسلسل الأقسام غير سليم)</li>
                <li>أقسام غير متوازنة (مثل مقدمة طويلة جداً ومناقشة قصيرة ومحدودة)</li>
                <li>عدم الالتزام بتعليمات النشر وقواعد التنسيق الخاصة بالمجلة (Author Guidelines)</li>
                <li>غموض في المصطلحات أو استخدام غير دقيق للمفاهيم</li>
            </ul>
            <h4>أمثلة من تعليقات المحكمين:</h4>
            <div class="example-box">
                <p>"البحث يحتاج إلى مراجعة لغوية شاملة؛ هناك أخطاء نحوية متعددة تؤثر على وضوح الأفكار وصعوبة متابعة الحجج."</p>
                <p>"تنظيم المقال ضعيف، مع تداخل بين الأقسام وتكرار غير ضروري للمعلومات. يصعب على القارئ متابعة الخيط المنطقي للبحث."</p>
                <p>"الملخص لا يعكس بدقة محتوى البحث والنتائج الرئيسية، كما أنه يتجاوز الحد المسموح به للكلمات."</p>
            </div>
            <h4>الحلول:</h4>
            <ol>
                <li>الاستعانة بمحرر لغوي متخصص (Native speaker editor إذا كانت الكتابة بلغة غير أم) قبل تقديم البحث</li>
                <li>طلب مراجعة الزملاء (Peer review) لمسودة البحث قبل التقديم</li>
                <li>استخدام هيكل واضح ومنطقي للبحث (مثل IMRaD)، مع عناوين فرعية مناسبة وفقرات مترابطة</li>
                <li>اتباع تعليمات النشر الخاصة بالمجلة بدقة (تنسيق، عدد كلمات، مراجع)</li>
                <li>كتابة الملخص بعد الانتهاء من كتابة البحث لضمان دقته وشموليته</li>
                <li>مراجعة البحث عدة مرات، مع التركيز في كل مرة على جانب مختلف (المحتوى، اللغة، التنسيق)</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)

	with st.expander("مراجعة أدبيات غير كافية (9%)"):
		st.markdown("""
        <div class="step-box">
            <h4>المشكلة:</h4>
            <p>قصور في مراجعة وتغطية الأدبيات ذات الصلة:</p>
            <ul>
                <li>عدم الإشارة إلى دراسات أساسية أو محورية (Seminal papers) في المجال</li>
                <li>الاعتماد على مصادر قديمة وإهمال الأدبيات الحديثة والتطورات الأخيرة</li>
                <li>مراجعة سطحية لا تحلل الدراسات السابقة بعمق، بل تكتفي بسردها</li>
                <li>عدم تحديد الفجوة البحثية (Research gap) بوضوح بناءً على الأدبيات</li>
                <li>ضعف الربط بين الأدبيات السابقة والدراسة الحالية (كيف يبني بحثك على ما سبق؟)</li>
            </ul>
            <h4>أمثلة من تعليقات المحكمين:</h4>
            <div class="example-box">
                <p>"لم يشر الباحثون إلى الأعمال الأساسية لـ (اسم باحث) التي تعتبر محورية في هذا المجال، مما يضعف الإطار النظري للبحث."</p>
                <p>"مراجعة الأدبيات تتوقف عند عام 2018، متجاهلة التطورات المهمة في السنوات الأخيرة والمناقشات الجارية حالياً."</p>
                <p>"مراجعة الأدبيات عبارة عن سرد للدراسات دون تحليل نقدي أو ربط بينها، ولم يتم توضيح كيف يساهم البحث الحالي في هذه الأدبيات."</p>
            </div>
            <h4>الحلول:</h4>
            <ol>
                <li>إجراء بحث منهجي وشامل للأدبيات، باستخدام قواعد بيانات متعددة (Scopus, Web of Science, EconLit)</li>
                <li>الاطلاع على أحدث الدراسات في المجال (آخر 3-5 سنوات) والمقالات المرجعية (Review articles)</li>
                <li>تنظيم مراجعة الأدبيات بشكل موضوعي أو منهجي، وليس مجرد سرد زمني</li>
                <li>تحليل الدراسات السابقة نقدياً، مع تحديد نقاط القوة والضعف والنتائج المتضاربة</li>
                <li>توضيح الفجوة البحثية التي يسعى بحثك لمعالجتها، وكيف يسدها</li>
                <li>الربط بوضوح بين الأدبيات السابقة وأسئلة بحثك ومنهجيتك وأهمية مساهمتك</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)

	with st.expander("أصالة البحث ومساهمته (8%)"):
		st.markdown("""
        <div class="step-box">
            <h4>المشكلة:</h4>
            <p>ضعف المساهمة العلمية الأصلية للبحث:</p>
            <ul>
                <li>تكرار لدراسات سابقة دون إضافة جديدة ملموسة (Incremental contribution is too small)</li>
                <li>نتائج متوقعة أو بديهية لا تضيف للمعرفة أو تثير اهتماماً كبيراً</li>
                <li>عدم وضوح الإضافة النظرية أو التطبيقية أو المنهجية للبحث</li>
                <li>مساهمة هامشية لا تبرر النشر في مجلة مرموقة</li>
                <li>موضوع قديم أو تم استهلاكه بحثياً دون تقديم زاوية جديدة</li>
            </ul>
            <h4>أمثلة من تعليقات المحكمين:</h4>
            <div class="example-box">
                <p>"البحث يكرر ما توصلت إليه دراسة (اسم الباحث) عام 2020، دون تقديم منظور جديد أو إضافة ملموسة. ما الجديد الذي يقدمه هذا البحث؟"</p>
                <p>"على الرغم من الجهد المبذول، فإن نتائج الدراسة متوقعة وتؤكد ما هو معروف بالفعل في المجال. المساهمة الحدية للبحث تبدو ضئيلة."</p>
                <p>"الباحثون لم يوضحوا بشكل كافٍ كيف يسهم بحثهم في تطوير النظرية أو الممارسة في مجال الاقتصاد. ما هي الآثار المترتبة على النتائج؟"</p>
            </div>
            <h4>الحلول:</h4>
            <ol>
                <li>تحديد وتوضيح المساهمة الفريدة لبحثك (نظرية، تجريبية، منهجية، بيانات جديدة) في مقدمة البحث وخاتمته</li>
                <li>التركيز على الجوانب المبتكرة في منهجيتك، بياناتك، أو نتائجك، أو تفسيراتك</li>
                <li>مقارنة نتائجك بالدراسات السابقة، مع توضيح ما تضيفه أو تختلف فيه أو تصححه</li>
                <li>تحديد الآثار النظرية والتطبيقية (Policy implications) لنتائجك بوضوح</li>
                <li>اختيار موضوعات بحثية تعالج فجوات حقيقية في المعرفة أو قضايا معاصرة مهمة</li>
                <li>مناقشة الاتجاهات المستقبلية للبحث بناءً على نتائجك، وكيف يفتح بحثك آفاقاً جديدة</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)

	with st.expander("إشكالية في تصميم البحث (3%)"):
		st.markdown("""
        <div class="step-box">
            <h4>المشكلة:</h4>
            <p>مشاكل أساسية في تصميم البحث تؤثر على صحة النتائج وموثوقيتها:</p>
            <ul>
                <li>عدم التوافق بين أسئلة البحث والتصميم المستخدم (e.g., using cross-sectional data for causal questions without proper methods)</li>
                <li>ضعف في تصميم التجارب (Experimental design) أو الاستبيانات (Survey design)</li>
                <li>عدم معالجة مشاكل التحيز المحتملة (Selection bias, endogeneity, omitted variable bias)</li>
                <li>قصور في تصميم أدوات جمع البيانات أو اختيار المقاييس (Measures)</li>
                <li>عدم وجود مجموعة ضابطة (Control group) مناسبة في الدراسات التجريبية أو شبه التجريبية</li>
            </ul>
            <h4>أمثلة من تعليقات المحكمين:</h4>
            <div class="example-box">
                <p>"التصميم البحثي المستخدم لا يسمح باختبار الفرضيات المطروحة بشكل دقيق، ولا يمكن استخلاص استنتاجات سببية من البيانات المقطعية بهذه الطريقة."</p>
                <p>"هناك مشكلة أساسية في تصميم الاستبيان، حيث تحتوي الأسئلة على تحيز في الصياغة (Leading questions) وقد تؤثر على إجابات المشاركين."</p>
                <p>"تصميم البحث لا يأخذ في الاعتبار المتغيرات الوسيطة (Mediating variables) أو المعدلة (Moderating variables) المهمة في العلاقة المدروسة، والتي تم تجاهلها."</p>
            </div>
            <h4>الحلول:</h4>
            <ol>
                <li>استشارة خبراء في تصميم البحوث أو الاقتصاد القياسي قبل بدء الدراسة</li>
                <li>اختبار أدوات البحث (مثل الاستبيان) على عينة تجريبية صغيرة (Pilot study) قبل التطبيق الكامل</li>
                <li>مراجعة الأدبيات المنهجية للتعرف على أفضل الممارسات في تصميم البحوث لنوع مشكلتك البحثية</li>
                <li>توضيح المبررات لاختيار التصميم البحثي المستخدم، والاعتراف بحدوده</li>
                <li>معالجة مصادر التحيز المحتملة في تصميم البحث والتحليل (e.g., using instrumental variables, difference-in-differences, RDD)</li>
                <li>تحديد القيود المرتبطة بالتصميم البحثي ومناقشتها بصراحة في قسم القيود (Limitations)</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)

	with st.expander("أخطاء إحصائية أو تحليلية (2%)"):
		st.markdown("""
        <div class="step-box">
            <h4>المشكلة:</h4>
            <p>أخطاء في التحليل الإحصائي أو تطبيق الأساليب التحليلية:</p>
            <ul>
                <li>استخدام اختبارات إحصائية غير مناسبة لنوع البيانات أو توزيعها</li>
                <li>أخطاء في تفسير النتائج الإحصائية (e.g., misinterpreting p-values, confusing correlation with causation)</li>
                <li>مشاكل في معالجة البيانات المفقودة (Missing data) أو القيم المتطرفة (Outliers)</li>
                <li>عدم التحقق من افتراضات (Assumptions) الاختبارات الإحصائية المستخدمة</li>
                <li>عدم إجراء اختبارات المتانة (Robustness checks) أو تحليل الحساسية (Sensitivity analysis)</li>
            </ul>
            <h4>أمثلة من تعليقات المحكمين:</h4>
            <div class="example-box">
                <p>"استخدام اختبار بارامتري (مثل t-test) مع بيانات لا تتبع التوزيع الطبيعي وحجم عينة صغير يجعل النتائج غير موثوقة. يجب استخدام اختبار لا بارامتري."</p>
                <p>"هناك خطأ في تفسير معاملات الانحدار في الجدول 4، حيث تم تفسيرها على أنها علاقات سببية، بينما النموذج لا يدعم هذا الاستنتاج."</p>
                <p>"لم يتم توضيح كيفية التعامل مع البيانات المفقودة، مما يثير تساؤلات حول تحيز النتائج. وماذا عن تأثير القيم المتطرفة؟"</p>
            </div>
            <h4>الحلول:</h4>
            <ol>
                <li>الاستعانة بخبير إحصائي أو اقتصادي قياسي لمراجعة خطة التحليل قبل تنفيذها وأثناء تفسير النتائج</li>
                <li>التحقق من ملاءمة الاختبارات الإحصائية لنوع البيانات (مستمرة، فئوية، رتبية) وأسئلة البحث</li>
                <li>التحقق من افتراضات الاختبارات الإحصائية قبل تطبيقها (e.g., normality, homoscedasticity, independence)</li>
                <li>توثيق خطوات معالجة البيانات بشفافية (التعامل مع البيانات المفقودة والقيم المتطرفة)</li>
                <li>تفسير النتائج الإحصائية بدقة وحذر، مع التمييز بين الدلالة الإحصائية والأهمية العملية/الاقتصادية</li>
                <li>تقديم تحليلات حساسية واختبارات متانة لاختبار مدى قوة النتائج تحت افتراضات أو مواصفات نموذج مختلفة</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)

	st.markdown("""
    <div class="warning-box">
        <h3>ملاحظة مهمة</h3>
        <p>غالباً ما يتم رفض البحث لأكثر من سبب واحد، وقد تتداخل هذه الأسباب. مثلاً، قد تؤدي المنهجية الضعيفة إلى نتائج غير مقنعة.
        من المهم النظر إلى تعليقات المحكمين بشكل شامل لتحديد المشاكل الرئيسية التي تحتاج إلى معالجة، وليس التركيز على نقطة واحدة فقط.</p>
    </div>
    """, unsafe_allow_html=True)


# صفحة أنواع الرفض
def rejection_types_page():
	st.title("أنواع قرارات الرفض في المجلات الاقتصادية")

	st.markdown("""
    <div class="info-box">
        <p>تتخذ المجلات العلمية عدة أنواع من قرارات الرفض، ولكل نوع دلالاته وكيفية التعامل معه.
        فهم نوع الرفض يساعدك على تحديد الخطوات المناسبة التالية لبحثك.</p>
    </div>
    """, unsafe_allow_html=True)

	st.subheader("توزيع أنواع قرارات الرفض")
	df_rejection_types_chart = pd.DataFrame({
		'نوع الرفض': rejection_types['نوع الرفض'],  # Raw
		'النسبة': rejection_types['النسبة المئوية']
	})
	fig_rejection_types = plot_arabic_pie_plotly(
		df_rejection_types_chart['النسبة'],
		df_rejection_types_chart['نوع الرفض'],  # Pass raw
		"توزيع أنواع قرارات الرفض في المجلات الاقتصادية",  # Pass raw
		'النسبة',
		'نوع الرفض'
	)
	st.plotly_chart(fig_rejection_types, use_container_width=True)

	st.subheader("مقارنة بين أنواع الرفض المختلفة")

	comparison_data_raw = {
		'نوع الرفض': rejection_types['نوع الرفض'],
		'الوصف': rejection_types['الوصف'],
		'المسؤول عن القرار': ['المحرر', 'المحكمون والمحرر', 'المحكمون والمحرر', 'المحرر بناءً على تقييم المحكمين'],
		'فرصة التقديم مجدداً': ['منخفضة جداً', 'منخفضة', 'مرتفعة (بعد تعديلات جوهرية)', 'منخفضة للمجلة نفسها'],
		'وقت الرد المتوقع': ['1-2 أسبوع', '2-4 أشهر', '2-4 أشهر', '2-4 أشهر']
	}
	# For DataFrames, pass raw Arabic strings. Streamlit should handle them with CSS.
	# If column headers need reshaping, do it for keys only.
	df_comparison = pd.DataFrame(comparison_data_raw)
	st.dataframe(df_comparison, hide_index=True, use_container_width=True)

	st.subheader("شرح تفصيلي لأنواع الرفض")

	with st.expander("رفض مباشر (Desk Rejection)"):  # Raw
		st.markdown("""
        <div class="step-box">
            <h4>التعريف:</h4>
            <p>هو رفض البحث من قبل محرر المجلة دون إرساله للتحكيم الخارجي. يحدث عادة خلال الأسبوع الأول أو الثاني من تقديم البحث (أحياناً أطول قليلاً).</p>
            <h4>الأسباب الشائعة:</h4>
            <ul>
                <li>عدم ملاءمة الموضوع لنطاق المجلة واهتماماتها (Out of scope).</li>
                <li>ضعف واضح في جودة البحث أو منهجيته (Fundamental flaws).</li>
                <li>عدم الالتزام بقواعد وإرشادات النشر في المجلة (e.g., formatting, length).</li>
                <li>مشاكل جوهرية في اللغة والكتابة تجعل من الصعب فهم البحث.</li>
                <li>عدم وضوح المساهمة العلمية للبحث أو مساهمة ضئيلة جداً (Lack of novelty/significance).</li>
                <li>تجاوز الحد الأقصى لعدد الكلمات أو الصفحات بشكل كبير.</li>
                <li>مشاكل أخلاقية واضحة (مثل الانتحال).</li>
            </ul>
            <h4>مثال لرسالة رفض مباشر:</h4>
            <div class="example-box">
                <p>"عزيزي الباحث/ة،</p>
                <p>نشكرك على تقديم بحثك "عنوان البحث" للنشر في مجلتنا. بعد المراجعة الأولية من قبل هيئة التحرير، وجدنا أن موضوع البحث لا يقع ضمن نطاق اهتمام المجلة المحدد. مجلتنا تركز على قضايا الاقتصاد الكلي والسياسات النقدية، بينما يركز بحثك على جوانب إدارية وتسويقية بشكل أساسي.</p>
                <p>لذلك، نأسف لإبلاغك بأننا لن نتمكن من إرسال بحثك لمزيد من المراجعة. نقترح عليك النظر في تقديم بحثك إلى مجلات متخصصة في الإدارة أو التسويق مثل [...] أو [...]. نتمنى لك التوفيق في نشر بحثك.</p>
                <p>مع خالص التقدير،</p>
                <p>محرر المجلة"</p>
            </div>
            <h4>كيفية التعامل مع الرفض المباشر:</h4>
            <ol>
                <li>لا تأخذ الرفض بشكل شخصي؛ هذا قرار شائع جداً لتوفير وقت المحكمين.</li>
                <li>اقرأ سبب الرفض بعناية واستفد منه في التحسين أو اختيار مجلة أخرى.</li>
                <li>إذا كان السبب هو عدم الملاءمة، ابحث عن مجلة أخرى أكثر تناسباً مع موضوع بحثك.</li>
                <li>إذا كان السبب يتعلق بجودة البحث، استشر زملاء ذوي خبرة لمراجعة البحث قبل إعادة تقديمه لمجلة أخرى.</li>
                <li>تأكد من الالتزام بإرشادات النشر للمجلة الجديدة التي ستقدم إليها البحث.</li>
            </ol>
            <h4>نصائح لتجنب الرفض المباشر:</h4>
            <ul>
                <li>اقرأ "نطاق وأهداف" المجلة (Aims and Scope) بعناية فائقة قبل التقديم.</li>
                <li>راجع عدة أعداد سابقة من المجلة لفهم نوعية الأبحاث التي تنشرها ومستواها.</li>
                <li>قم بإعداد "خطاب تقديم" (Cover Letter) قوي ومقنع يشرح بوضوح أهمية بحثك ومناسبته للمجلة.</li>
                <li>اطلب من زميل خبير مراجعة بحثك (خاصة الملخص والمقدمة) قبل التقديم.</li>
                <li>في حالة الشك، يمكن مراسلة محرر المجلة مسبقاً (Pre-submission inquiry) للاستفسار عن ملاءمة الموضوع.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
	# ... (Repeat for other expanders, using raw Arabic strings for titles) ...
	with st.expander("رفض بعد التحكيم (Rejection after Review)"):
		st.markdown("""
        <div class="step-box">
            <h4>التعريف:</h4>
            <p>رفض البحث بعد مروره بعملية التحكيم الخارجي (Peer review)، بناءً على تقييمات المحكمين وقرار المحرر. يأتي هذا القرار عادة بعد 2-4 أشهر (أو أكثر) من تقديم البحث.</p>
            <h4>الأسباب الشائعة:</h4>
            <ul>
                <li>مشاكل جوهرية في المنهجية أو التصميم البحثي.</li>
                <li>ضعف المساهمة العلمية أو عدم أصالة البحث.</li>
                <li>نتائج غير مقنعة، غير مدعومة بشكل كافٍ، أو غير متينة.</li>
                <li>ضعف في التحليل الإحصائي أو تفسير النتائج.</li>
                <li>مراجعة أدبيات غير كافية، غير محدثة، أو سطحية.</li>
                <li>تعارض كبير بين تقييمات المحكمين مع ترجيح المحرر جانب الرفض.</li>
                <li>عدم القدرة على معالجة ملاحظات المحكمين بشكل مرضٍ (في حالة المراجعات المتعددة).</li>
            </ul>
            <h4>مثال لرسالة رفض بعد التحكيم:</h4>
            <div class="example-box">
                <p>"عزيزي الباحث/ة،</p>
                <p>بعد مراجعة دقيقة لبحثك "عنوان البحث" من قبل ثلاثة محكمين متخصصين، نأسف لإبلاغك أننا غير قادرين على قبول بحثك للنشر في مجلتنا في صيغته الحالية.</p>
                <p>على الرغم من أن المحكمين أشادوا بأهمية الموضوع والدقة في جمع البيانات، إلا أنهم أثاروا مخاوف جوهرية حول المنهجية المستخدمة وكفاية حجم العينة لدعم الاستنتاجات المقدمة. كما أشار المحكمون إلى ضرورة تحديث مراجعة الأدبيات لتشمل الدراسات الحديثة في المجال، وتقديم تحليل أكثر عمقاً للآثار المترتبة على النتائج.</p>
                <p>نرفق طياً تقارير المحكمين الثلاثة، ونأمل أن تكون مفيدة في تطوير بحثك. نشجعك على مراجعة هذه التعليقات بعناية والنظر في إجراء التعديلات اللازمة قبل التقديم إلى مجلة أخرى.</p>
                <p>نشكرك على اهتمامك بمجلتنا ونتمنى لك التوفيق في مساعيك البحثية المستقبلية.</p>
                <p>مع خالص التقدير،</p>
                <p>محرر المجلة"</p>
            </div>
            <h4>كيفية التعامل مع الرفض بعد التحكيم:</h4>
            <ol>
                <li>خذ وقتاً كافياً لاستيعاب القرار والتعامل مع الإحباط الأولي (يوم أو يومين).</li>
                <li>اقرأ تعليقات المحكمين بعناية وحياد، وصنفها حسب أهميتها وقابليتها للتنفيذ.</li>
                <li>ناقش التعليقات مع المشاركين في البحث أو مع زملاء لديهم خبرة.</li>
                <li>حدد ما إذا كانت المشاكل المذكورة يمكن معالجتها أم أنها تتطلب إعادة تصميم البحث أو جمع بيانات جديدة.</li>
                <li>قم بإجراء التعديلات اللازمة وحسّن البحث بناءً على التعليقات، حتى لو قررت التقديم لمجلة أخرى.</li>
                <li>ابحث عن مجلة أخرى مناسبة لموضوع بحثك ومستواه بعد التعديل.</li>
                <li>في حالة التقديم لمجلة جديدة، أشر في خطاب التقديم إلى التحسينات التي أجريتها بناءً على تعليقات المحكمين السابقين (إذا كان ذلك مناسباً).</li>
            </ol>
            <h4>نصائح للاستفادة من تعليقات المحكمين:</h4>
            <ul>
                <li>افصل بين انفعالاتك الشخصية والتقييم الموضوعي للتعليقات.</li>
                <li>ركز على التعليقات المتكررة من أكثر من محكم، فهي غالباً تشير إلى مشاكل حقيقية.</li>
                <li>ابحث عن الأنماط في التعليقات، مثل التركيز على قسم معين من البحث أو مشكلة منهجية معينة.</li>
                <li>استخدم التعليقات كفرصة للتعلم وتطوير مهاراتك البحثية والكتابية.</li>
                <li>احتفظ بسجل للتعليقات المتكررة لتجنب نفس المشاكل في أبحاثك المستقبلية.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

	with st.expander("رفض مع إمكانية إعادة التقديم (Reject and Resubmit)"):
		st.markdown("""
        <div class="step-box">
            <h4>التعريف:</h4>
            <p>رفض البحث بصيغته الحالية، مع دعوة صريحة من المحرر لإعادة تقديمه بعد إجراء تعديلات جوهرية. يختلف عن "تعديلات رئيسية" (Major Revisions) في أن المحرر لا يضمن قبول البحث حتى بعد التعديلات، وسيتم تقييمه كتقديم جديد (وقد يرسل لنفس المحكمين أو محكمين جدد).</p>
            <h4>الأسباب الشائعة:</h4>
            <ul>
                <li>البحث يتناول موضوعاً مهماً وله إمكانات، لكنه يحتاج إلى تحسينات جوهرية لا يمكن اعتبارها "تعديلات".</li>
                <li>الحاجة إلى تغييرات كبيرة في المنهجية، جمع بيانات إضافية، أو إجراء تحليلات جديدة ومعقدة.</li>
                <li>ضرورة إعادة هيكلة البحث بشكل كبير أو تغيير تركيزه أو توسيع نطاقه.</li>
                <li>مشاكل في الإطار النظري أو التحليل تتطلب إعادة صياغة وتفكير عميق.</li>
            </ul>
            <h4>مثال لرسالة رفض مع إمكانية إعادة التقديم:</h4>
            <div class="example-box">
                <p>"عزيزي الباحث/ة،</p>
                <p>لقد تمت مراجعة بحثك "عنوان البحث" من قبل ثلاثة محكمين متخصصين. استناداً إلى تقييماتهم وتقييمي الشخصي، لا يمكننا قبول البحث بصيغته الحالية للنشر في مجلتنا.</p>
                <p>ومع ذلك، يرى المحكمون والمحرر أن موضوع البحث مهم وله إمكانات كبيرة. لذلك، نشجعك على إعادة تقديم نسخة معدلة بشكل جوهري من البحث تعالج المشاكل المذكورة في تقارير المحكمين المرفقة، وخاصة:</p>
                <ol>
                    <li>توسيع حجم العينة بشكل كبير ليكون أكثر تمثيلاً للمجتمع المستهدف، وربما إضافة بيانات طولية.</li>
                    <li>إعادة تصميم المنهجية لمعالجة مشاكل الداخلية (Endogeneity) المحتملة التي أشار إليها المحكمون.</li>
                    <li>تحديث مراجعة الأدبيات لتشمل النظريات الحديثة (بعد 2020) ودمجها بشكل أعمق في الإطار النظري.</li>
                    <li>تقديم تحليلات إحصائية إضافية، بما في ذلك اختبارات المتانة وتحليل المجموعات الفرعية.</li>
                </ol>
                <p>يرجى ملاحظة أن إعادة التقديم ستعامل كتقديم جديد وستخضع لعملية تحكيم كاملة. نرجو أن ترفق مع إعادة التقديم رسالة تفصيلية (point-by-point response) توضح التغييرات التي أجريتها استجابةً لتعليقات المحكمين. إذا قررت إعادة التقديم، يرجى القيام بذلك خلال [فترة زمنية، مثلاً 6 أشهر].</p>
                <p>نتطلع إلى استلام النسخة المعدلة من بحثك في المستقبل.</p>
                <p>مع خالص التقدير،</p>
                <p>محرر المجلة"</p>
            </div>
            <h4>كيفية التعامل مع الرفض مع إمكانية إعادة التقديم:</h4>
            <ol>
                <li>اعتبر هذا القرار فرصة إيجابية ومشجعة؛ فالمحرر يرى إمكانات كبيرة في بحثك.</li>
                <li>قم بتحليل تعليقات المحكمين بدقة وصنفها حسب الأهمية والجهد المطلوب.</li>
                <li>ضع خطة عمل تفصيلية للتعديلات المطلوبة، مع جدول زمني واقعي.</li>
                <li>تشاور مع زملاء أو خبراء في المجالات التي تحتاج إلى تحسين (منهجية، إحصاء).</li>
                <li>أجرِ التعديلات الجوهرية المطلوبة بجدية، حتى لو استغرق ذلك وقتاً طويلاً وجهداً كبيراً.</li>
                <li>أعد صياغة أجزاء كبيرة من البحث إذا لزم الأمر، لا تكتفِ بتعديلات سطحية.</li>
                <li>عند إعادة التقديم، أرفق رسالة مفصلة ومنظمة (Response to reviewers) توضح التغييرات التي أجريتها استجابةً لكل نقطة من تعليقات المحكمين.</li>
            </ol>
            <h4>نصائح لزيادة فرص القبول عند إعادة التقديم:</h4>
            <ul>
                <li>تعامل مع جميع النقاط المثارة في تقارير المحكمين بجدية، حتى التي لا تتفق معها (اشرح وجهة نظرك بأدب).</li>
                <li>قدم تبريرات علمية واضحة في حالة عدم تنفيذ بعض الاقتراحات.</li>
                <li>استشهد بالأدبيات الجديدة التي ظهرت منذ التقديم الأول.</li>
                <li>تأكد من تحسين جودة الكتابة والتحرير بالإضافة إلى المحتوى العلمي.</li>
                <li>اطلب من زملاء لم يطلعوا على البحث سابقاً قراءة النسخة المعدلة وتقديم ملاحظاتهم.</li>
                <li>التزم بالمدة الزمنية المقترحة لإعادة التقديم إن وجدت.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

	with st.expander("رفض مع التشجيع على التقديم لمجلة أخرى"):
		st.markdown("""
        <div class="step-box">
            <h4>التعريف:</h4>
            <p>رفض البحث مع تقديم اقتراحات محددة بمجلات بديلة قد تكون أكثر ملاءمة لموضوع البحث أو مستواه أو منهجيته. قد يشمل هذا النوع توصية من المحرر إلى محرر المجلة المقترحة (أحياناً).</p>
            <h4>الأسباب الشائعة:</h4>
            <ul>
                <li>البحث خارج نطاق اهتمام المجلة لكنه جيد من الناحية العلمية.</li>
                <li>مستوى البحث (مثلاً، مساهمة محدودة أو نطاق ضيق) لا يتناسب مع المستوى المرتفع للمجلة المقدم إليها، ولكنه مناسب لمجلة أخرى.</li>
                <li>الموضوع أكثر تخصصاً أو أكثر عمومية مما تنشره المجلة عادة.</li>
                <li>نطاق البحث محلي أو إقليمي بينما المجلة تفضل الأبحاث ذات النطاق العالمي (أو العكس).</li>
                <li>أسلوب البحث (نظري، تجريبي، نوعي) لا يتوافق مع توجه المجلة.</li>
            </ul>
            <h4>مثال لرسالة رفض مع التشجيع على التقديم لمجلة أخرى:</h4>
            <div class="example-box">
                <p>"عزيزي الباحث/ة،</p>
                <p>شكراً على تقديم بحثك "عنوان البحث" للنشر في مجلة الاقتصاد العالمي. بعد مراجعة دقيقة من قبل المحكمين والمحررين، نأسف لإبلاغك أننا لا نستطيع قبول بحثك للنشر.</p>
                <p>على الرغم من أن البحث يتميز بمنهجية سليمة وتحليل جيد، إلا أن تركيزه على الاقتصاد المحلي لدولة نامية واحدة يجعله أقل ملاءمة لمجلتنا التي تركز بشكل أساسي على قضايا الاقتصاد العالمي والعلاقات الاقتصادية بين الدول المتقدمة والتكتلات الكبرى.</p>
                <p>نعتقد أن بحثك قد يكون مناسباً جداً لمجلة "اقتصاديات التنمية والتغيير" أو "مجلة دراسات التنمية الإقليمية"، حيث يتوافق موضوعه مع اهتماماتهما البحثية. يمكنك الاطلاع على تقارير المحكمين المرفقة والاستفادة منها في تحسين البحث قبل تقديمه لمجلة أخرى.</p>
                <p>نشكرك على اهتمامك بمجلتنا ونتمنى لك التوفيق في نشر بحثك.</p>
                <p>مع خالص التقدير،</p>
                <p>محرر المجلة"</p>
            </div>
            <h4>كيفية التعامل مع الرفض مع التشجيع على التقديم لمجلة أخرى:</h4>
            <ol>
                <li>اعتبر هذا النوع من الرفض إيجابياً نسبياً؛ فهو يشير إلى أن البحث له قيمة علمية ولكن في مكان غير مناسب.</li>
                <li>ابحث عن المجلات المقترحة بعناية (اقرأ نطاقها، أهدافها، الأبحاث المنشورة فيها).</li>
                <li>إذا عرض المحرر إرسال توصية إلى محرر المجلة المقترحة، استفد من هذا العرض (هذا نادر).</li>
                <li>قم بتعديل البحث ليتناسب مع متطلبات وأسلوب المجلة الجديدة (لا تقدم نفس النسخة تماماً).</li>
                <li>عند التقديم للمجلة الجديدة، يمكنك الإشارة في خطاب التقديم إلى توصية محرر المجلة السابقة (إذا كانت التوصية واضحة وإيجابية).</li>
                <li>استفد من تعليقات المحكمين لتحسين البحث قبل تقديمه للمجلة الجديدة.</li>
            </ol>
            <h4>نصائح للاستفادة من هذا النوع من الرفض:</h4>
            <ul>
                <li>استفد من تعليقات المحكمين لتحسين البحث قبل تقديمه للمجلة الجديدة.</li>
                <li>اقرأ عدة أعداد من المجلة المقترحة لفهم أسلوبها ومتطلباتها وجمهورها.</li>
                <li>عدّل عنوان البحث وملخصه ومقدمته لتعكس اهتمامات المجلة الجديدة وتبرز ملاءمته لها.</li>
                <li>تواصل مع محرر المجلة الجديدة (Pre-submission inquiry) قبل التقديم للتأكد من ملاءمة البحث.</li>
                <li>استخدم هذه التجربة لتحسين استراتيجية اختيار المجلات المناسبة لأبحاثك المستقبلية.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

	st.markdown("""
    <div class="success-box">
        <h3>فرص النجاح بعد الرفض</h3>
        <p>أظهرت دراسات (مثل تلك التي نشرت في JAMA أو Nature) أن نسبة كبيرة من الأبحاث المرفوضة يتم نشرها لاحقاً:</p>
        <ul>
            <li>حوالي <strong>50-60%</strong> من الأبحاث المرفوضة من مجلات مرموقة تُنشر في نهاية المطاف في مجلات أخرى (قد تكون أقل تأثيراً أو أكثر تخصصاً).</li>
            <li>الأبحاث التي تتلقى قرار "رفض مع إمكانية إعادة التقديم" لديها فرصة قبول أعلى بكثير (قد تصل إلى <strong>60-70%</strong>) إذا تم التعامل مع ملاحظات المحكمين بجدية.</li>
            <li>الغالبية العظمى من الباحثين (أكثر من <strong>75%</strong>) يؤكدون أن جودة أبحاثهم تحسنت بشكل ملحوظ نتيجة لتعليقات المحكمين، حتى في حالة الرفض النهائي من المجلة الأولى.</li>
        </ul>
        <p>لا تدع قرار الرفض يثبط عزيمتك، بل اعتبره خطوة ضرورية في عملية صقل البحث وتحسينه!</p>
    </div>
    """, unsafe_allow_html=True)


# صفحة تحليل تعليقات المحكمين
def reviewers_comments_page():
	st.title("تحليل تعليقات المحكمين وكيفية فهمها")

	st.markdown("""
    <div class="info-box">
        <p>تعليقات المحكمين هي مصدر قيّم للتعلم وتحسين البحث، حتى في حالة الرفض. 
        فهم هذه التعليقات وتصنيفها وتحديد أولويات التعامل معها يعتبر مهارة أساسية للباحثين.</p>
    </div>
    """, unsafe_allow_html=True)

	st.subheader("أنواع تعليقات المحكمين ونسبتها")
	df_comments_chart = pd.DataFrame({
		'نوع التعليق': reviewers_comments['نوع التعليق'],  # Raw
		'النسبة': reviewers_comments['النسبة المئوية']
	})
	fig_reviewers_comments = plot_arabic_pie_plotly(
		df_comments_chart['النسبة'],
		df_comments_chart['نوع التعليق'],  # Pass raw
		"توزيع أنواع تعليقات المحكمين في المجلات الاقتصادية",  # Pass raw
		'النسبة',
		'نوع التعليق'
	)
	st.plotly_chart(fig_reviewers_comments, use_container_width=True)

	st.subheader("تفصيل أنواع تعليقات المحكمين وأمثلة عليها")

	for i in range(len(reviewers_comments['نوع التعليق'])):
		expander_title = f"{reviewers_comments['نوع التعليق'][i]} ({reviewers_comments['النسبة المئوية'][i]}%)"  # Raw
		with st.expander(expander_title):
			examples_raw = reviewers_comments['الأمثلة'][i].split(" • ")
			# examples_reshaped = [get_display(arabic_reshaper.reshape(ex)) for ex in examples_raw] # No reshaping here for markdown

			st.markdown(f"""
            <div class="step-box">
                <h4>أمثلة على هذا النوع من التعليقات:</h4>
                <ul>
                    {"".join([f"<li>{example}</li>" for example in examples_raw])}
                </ul>
            </div>
            """, unsafe_allow_html=True)

	st.subheader("استراتيجيات فهم وتحليل تعليقات المحكمين")

	with st.expander("كيفية تصنيف تعليقات المحكمين"):  # Raw
		st.markdown("""
        <div class="step-box">
            <p>من المفيد تصنيف تعليقات المحكمين لتسهيل التعامل معها وتحديد الأولويات. يمكنك استخدام جدول بسيط لتنظيم التعليقات:</p>
            <h4>1. التصنيف حسب الأهمية (Severity):</h4>
            <ul>
                <li><strong>تعليقات حاسمة (Fatal flaws):</strong> مشاكل جوهرية يجب معالجتها بالكامل وإلا سيرفض البحث (مثل أخطاء منهجية كبيرة، مساهمة غير واضحة).</li>
                <li><strong>تعليقات مهمة (Major concerns):</strong> مشاكل كبيرة تؤثر على جودة البحث وثقة النتائج، وتحتاج لمعالجة جادة (مثل توسيع العينة، تحليلات إضافية).</li>
                <li><strong>تعليقات ثانوية (Minor suggestions):</strong> اقتراحات لتحسين البحث ولكنها ليست ضرورية لقبوله (مثل تحسينات لغوية طفيفة، إضافة مرجع، توضيح بسيط).</li>
            </ul>
            <h4>2. التصنيف حسب القسم المتعلق بالبحث:</h4>
            <ul>
                <li>تعليقات على العنوان والملخص والمقدمة والإطار النظري.</li>
                <li>تعليقات على مراجعة الأدبيات.</li>
                <li>تعليقات على المنهجية (التصميم، العينة، الأدوات، جمع البيانات).</li>
                <li>تعليقات على النتائج والتحليل الإحصائي.</li>
                <li>تعليقات على المناقشة والاستنتاجات والتوصيات.</li>
                <li>تعليقات على اللغة والتنسيق والمراجع.</li>
            </ul>
            <h4>3. التصنيف حسب سهولة المعالجة (Feasibility):</h4>
            <ul>
                <li><strong>سهلة المعالجة:</strong> يمكن تنفيذها بسرعة ودون جهد كبير (مثل التصحيحات اللغوية، تعديل جملة).</li>
                <li><strong>متوسطة المعالجة:</strong> تتطلب جهداً ووقتاً متوسطاً (مثل إضافة تحليلات إضافية ببيانات موجودة، مراجعة قسم من الأدبيات).</li>
                <li><strong>صعبة المعالجة:</strong> تتطلب تغييرات جذرية، إعادة جمع بيانات، أو تعلم مهارات جديدة (مثل تغيير المنهجية بالكامل، جمع بيانات طولية).</li>
            </ul>
            <h4>4. التصنيف حسب الاتفاق بين المحكمين:</h4>
            <ul>
                <li><strong>تعليقات متفق عليها:</strong> ذكرها أكثر من محكم (أولوية عالية).</li>
                <li><strong>تعليقات فردية:</strong> ذكرها محكم واحد فقط (تحتاج تقييم دقيق).</li>
                <li><strong>تعليقات متضاربة:</strong> تعليقات متناقضة بين المحكمين (تحتاج قرار وتبرير).</li>
            </ul>
            <div class="example-box">
                <h4>مثال لجدول تصنيف التعليقات:</h4>
                <table style="width:100%; border-collapse: collapse; text-align: right; direction: rtl; font-size: 0.9em;">
                    <tr style="background-color: #f2f2f2;">
                        <th style="border: 1px solid #ddd; padding: 8px;">التعليق (مختصر)</th>
                        <th style="border: 1px solid #ddd; padding: 8px;">المحكم</th>
                        <th style="border: 1px solid #ddd; padding: 8px;">الأهمية</th>
                        <th style="border: 1px solid #ddd; padding: 8px;">القسم</th>
                        <th style="border: 1px solid #ddd; padding: 8px;">سهولة المعالجة</th>
                        <th style="border: 1px solid #ddd; padding: 8px;">ملاحظات/خطة الرد</th>
                    </tr>
                    <tr>
                        <td style="border: 1px solid #ddd; padding: 8px;">حجم العينة صغير جداً (N=32)</td>
                        <td style="border: 1px solid #ddd; padding: 8px;">م1, م2</td>
                        <td style="border: 1px solid #ddd; padding: 8px;">حاسمة</td>
                        <td style="border: 1px solid #ddd; padding: 8px;">المنهجية</td>
                        <td style="border: 1px solid #ddd; padding: 8px;">صعبة</td>
                        <td style="border: 1px solid #ddd; padding: 8px;">محاولة جمع بيانات إضافية، أو تبرير العينة الحالية ومناقشة القيود بوضوح.</td>
                    </tr>
                    <tr>
                        <td style="border: 1px solid #ddd; padding: 8px;">مراجعة الأدبيات لا تشمل دراسات ما بعد 2020</td>
                        <td style="border: 1px solid #ddd; padding: 8px;">م1</td>
                        <td style="border: 1px solid #ddd; padding: 8px;">مهمة</td>
                        <td style="border: 1px solid #ddd; padding: 8px;">مراجعة الأدبيات</td>
                        <td style="border: 1px solid #ddd; padding: 8px;">متوسطة</td>
                        <td style="border: 1px solid #ddd; padding: 8px;">تحديث المراجعة وإضافة الدراسات الحديثة.</td>
                    </tr>
                    <tr>
                        <td style="border: 1px solid #ddd; padding: 8px;">أخطاء لغوية متعددة</td>
                        <td style="border: 1px solid #ddd; padding: 8px;">م3</td>
                        <td style="border: 1px solid #ddd; padding: 8px;">ثانوية (لكن مهمة للوضوح)</td>
                        <td style="border: 1px solid #ddd; padding: 8px;">اللغة والتنسيق</td>
                        <td style="border: 1px solid #ddd; padding: 8px;">سهلة/متوسطة</td>
                        <td style="border: 1px solid #ddd; padding: 8px;">مراجعة لغوية شاملة أو الاستعانة بمحرر.</td>
                    </tr>
                </table>
            </div>
        </div>
        """, unsafe_allow_html=True)
	# ... (Repeat for other expanders, using raw Arabic strings for titles) ...
	with st.expander("كيفية التعامل مع التعليقات المتناقضة"):
		st.markdown("""
        <div class="step-box">
            <p>من الشائع أن تتلقى تعليقات متناقضة من المحكمين، وهذا يمثل تحدياً في كيفية الاستجابة لها:</p>
            <h4>أنواع التناقضات الشائعة:</h4>
            <ul>
                <li>تناقض في تقييم جودة جزء معين من البحث (أحدهم يراه جيداً والآخر ضعيفاً).</li>
                <li>تناقض في التوصيات المقترحة للتحسين (أحدهم يقترح توسيع النطاق والآخر تضييقه).</li>
                <li>تناقض في التقييم العام للبحث (أحدهم يوصي بالقبول والآخر بالرفض).</li>
                <li>تناقض في تقييم أهمية البحث ومساهمته.</li>
            </ul>
            <h4>استراتيجيات التعامل مع التعليقات المتناقضة:</h4>
            <ol>
                <li><strong>الرجوع إلى تعليق المحرر:</strong> غالباً ما يقدم المحرر توجيهاً أو يرجح كفة أحد المحكمين، أو يلخص النقاط الرئيسية التي يجب التركيز عليها.</li>
                <li><strong>البحث عن نقاط الاتفاق:</strong> حدد النقاط التي اتفق عليها المحكمون (حتى لو اختلفوا في أمور أخرى)، وابدأ بمعالجتها.</li>
                <li><strong>التوفيق بين وجهات النظر:</strong> حاول إيجاد حل وسط يلبي (ولو جزئياً) مخاوف جميع المحكمين إذا أمكن.</li>
                <li><strong>تقديم حجج علمية لاختيارك:</strong> في حالة الاضطرار للاختيار بين توصيات متناقضة، قدم أسباباً علمية ومنطقية لاختيارك، مدعومة بالأدبيات إن أمكن.</li>
                <li><strong>معالجة جميع التعليقات:</strong> اشرح في ردك كيف تعاملت مع كل تعليق، حتى المتناقضة منها. وضح لماذا فضلت رأياً على آخر.</li>
                <li><strong>الشفافية مع المحرر:</strong> في رسالة الرد، يمكنك الإشارة بوضوح إلى التناقض وكيف حاولت حله.</li>
            </ol>
            <div class="example-box">
                <h4>مثال على التعامل مع تعليقات متناقضة:</h4>
                <p><strong>المحكم 1:</strong> "يجب توسيع عينة الدراسة لتشمل المزيد من الدول النامية لزيادة القدرة على تعميم النتائج."</p>
                <p><strong>المحكم 2:</strong> "أقترح التركيز على عدد أقل من الدول وتعميق التحليل ودراسة الحالة بدلاً من التوسع الأفقي الذي قد يضعف عمق التحليل."</p>
                <p><strong>كيفية الرد (مثال):</strong></p>
                <blockquote>
                    "نشكر المحكمين على ملاحظاتهم القيمة حول نطاق العينة. بعد دراسة متأنية للتعليقات المتناقضة، قررنا اتباع نهج متوازن يأخذ في الاعتبار كلا المنظورين:
                    <br><br>
                    1. حافظنا على التركيز العميق على الدول الخمس الأصلية في العينة، وأضفنا تحليلات نوعية معمقة لهذه الحالات (استجابة لروح تعليق المحكم 2).
                    <br>
                    2. لتلبية الحاجة إلى تعميم أكبر (كما أشار المحكم 1)، قمنا بإضافة تحليل تكميلي يستند إلى بيانات ثانوية مجمعة لمجموعة أوسع من 20 دولة نامية، لمقارنة الاتجاهات العامة مع نتائجنا التفصيلية.
                    <br>
                    3. ناقشنا القيود المترتبة على هذا النهج المختلط، وأوضحنا أن التعميم الكامل يتطلب دراسات مستقبلية أوسع نطاقاً.
                    <br><br>
                    نعتقد أن هذا النهج يحقق توازناً بين عمق التحليل وسعة النطاق، مع الأخذ في الاعتبار القيود العملية للبحث الحالي والموارد المتاحة."
                </blockquote>
            </div>
        </div>
        """, unsafe_allow_html=True)

	with st.expander("كيفية قراءة ما بين السطور في تعليقات المحكمين"):
		st.markdown("""
        <div class="step-box">
            <p>غالباً ما تحمل تعليقات المحكمين رسائل ضمنية وإشارات غير مباشرة يجب فهمها للاستجابة بشكل فعال. المحكمون قد يستخدمون لغة دبلوماسية لتخفيف حدة النقد:</p>
            <h4>عبارات شائعة ودلالاتها المحتملة:</h4>
            <table style="width:100%; border-collapse: collapse; text-align: right; direction: rtl; font-size: 0.9em;">
                <tr style="background-color: #f2f2f2;">
                    <th style="border: 1px solid #ddd; padding: 8px;">العبارة التي قد يستخدمها المحكم</th>
                    <th style="border: 1px solid #ddd; padding: 8px;">الدلالة المحتملة (ما يعنيه المحكم حقاً)</th>
                </tr>
                <tr>
                    <td style="border: 1px solid #ddd; padding: 8px;">"البحث مثير للاهتمام، ولكن..."</td>
                    <td style="border: 1px solid #ddd; padding: 8px;">الفكرة جيدة، لكن التنفيذ ضعيف أو هناك مشاكل جوهرية تحتاج إلى معالجة. (التركيز على ما بعد "ولكن").</td>
                </tr>
                <tr>
                    <td style="border: 1px solid #ddd; padding: 8px;">"قد يرغب الباحثون في النظر في..." أو "ربما يكون من المفيد..."</td>
                    <td style="border: 1px solid #ddd; padding: 8px;">هذه ليست مجرد اقتراحات اختيارية، بل توصيات قوية يجب أخذها على محمل الجد. تجاهلها قد يكون خطيراً.</td>
                </tr>
                <tr>
                    <td style="border: 1px solid #ddd; padding: 8px;">"من غير الواضح كيف توصل الباحثون إلى..." أو "الحجة هنا غير مقنعة."</td>
                    <td style="border: 1px solid #ddd; padding: 8px;">هناك مشكلة في الشرح، أو المنطق، أو الأدلة المقدمة. تحتاج إلى توضيح كبير أو إعادة تفكير.</td>
                </tr>
                <tr>
                    <td style="border: 1px solid #ddd; padding: 8px;">"الأدبيات في هذا المجال واسعة ومتنوعة..."</td>
                    <td style="border: 1px solid #ddd; padding: 8px;">مراجعة الأدبيات الخاصة بك غير كافية، أو سطحية، أو تجاهلت دراسات مهمة أو تيارات فكرية رئيسية.</td>
                </tr>
                <tr>
                    <td style="border: 1px solid #ddd; padding: 8px;">"النتائج ليست مفاجئة (not surprising) وتؤكد ما هو معروف."</td>
                    <td style="border: 1px solid #ddd; padding: 8px;">المساهمة العلمية للبحث محدودة أو ضعيفة. البحث لا يقدم إضافة نوعية للمعرفة.</td>
                </tr>
                 <tr>
                    <td style="border: 1px solid #ddd; padding: 8px;">"أقترح بعض التعديلات الطفيفة." (في سياق تقرير سلبي عموماً)</td>
                    <td style="border: 1px solid #ddd; padding: 8px;">قد يكون المحكم يحاول تلطيف الرفض، أو أن المشاكل الأساسية كبيرة جداً لدرجة أن التعديلات "الطفيفة" لن تكون كافية.</td>
                </tr>
            </table>
            <h4>نصائح لفهم الرسائل الضمنية:</h4>
            <ol>
                <li>انتبه لتكرار الإشارة إلى جانب معين من أكثر من محكم، أو من نفس المحكم في مواضع مختلفة.</li>
                <li>لاحظ درجة التفصيل في التعليق؛ كلما كان التعليق أكثر تفصيلاً وتحديداً، كان أكثر أهمية وجدية.</li>
                <li>انتبه للغة المستخدمة؛ كلمات مثل "ربما"، "قد"، "من الممكن" غالباً ما تخفي توصيات قوية يجب التعامل معها بجدية.</li>
                <li>اقرأ تقييم كل محكم ككل (بما في ذلك التوصية النهائية للمحرر) لفهم وجهة نظره العامة ومدى رضاه عن البحث.</li>
                <li>قارن بين تعليقات المحكمين المختلفين للحصول على صورة أوضح للنقاط الحاسمة.</li>
            </ol>
            <div class="example-box">
                <h4>مثال على قراءة ما بين السطور:</h4>
                <p><strong>تعليق المحكم:</strong> "البحث يتناول موضوعاً مهماً، ومنهجيته مناسبة بشكل عام. ومع ذلك، قد يرغب الباحثون في النظر في توسيع عينة الدراسة لتشمل قطاعات اقتصادية متنوعة، حيث أن الأدبيات الحديثة في هذا المجال تشير إلى أهمية التنوع القطاعي في العينات لدراسة هذه الظاهرة."</p>
                <p><strong>القراءة بين السطور:</strong></p>
                <ul>
                    <li><strong>"موضوع مهم، منهجية مناسبة بشكل عام":</strong> بداية إيجابية، لكنها تمهيد للنقد.</li>
                    <li><strong>"قد يرغب الباحثون في النظر في...":</strong> هذه ليست مجرد رغبة، بل توصية قوية جداً بأن العينة الحالية (التي ربما تفتقر للتنوع القطاعي) هي نقطة ضعف رئيسية.</li>
                    <li><strong>"الأدبيات الحديثة... تشير إلى أهمية التنوع":</strong> المحكم يشير ضمناً إلى أن الباحث لم يطلع جيداً على الأدبيات الحديثة، أو أن تصميمه لا يتماشى مع أفضل الممارسات الحالية.</li>
                    <li><strong>الرسالة الكلية:</strong> المحكم يرى أن البحث له إمكانات، ولكن مشكلة العينة (وقصور محتمل في مراجعة الأدبيات) يجب معالجتها بجدية. تجاهل هذه النقطة قد يؤدي للرفض.</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)

	st.subheader("أداة تصنيف تعليقات المحكمين (نموذج بسيط)")

	st.markdown("""
    <div class="info-box">
        <p>أدخل تعليقات المحكمين هنا للمساعدة في تصنيفها وتحديد أولويات التعامل معها. هذه أداة بسيطة للتفكير المنظم.</p>
    </div>
    """, unsafe_allow_html=True)

	if 'comments_list' not in st.session_state:
		st.session_state.comments_list = []

	with st.form("comment_form", clear_on_submit=True):
		reviewer_comment_text = st.text_area("أدخل تعليق المحكم (أو جزء منه):", height=100)  # Raw label

		col1_form, col2_form, col3_form = st.columns(3)
		with col1_form:
			importance_val = st.selectbox("أهمية التعليق:",  # Raw label
										  ["حاسمة", "مهمة", "ثانوية"], key="importance_raw")  # Raw options
		with col2_form:
			section_val = st.selectbox("القسم المتعلق:",  # Raw label
									   ["المقدمة/الإطار النظري", "مراجعة الأدبيات", "المنهجية/التصميم",
										"النتائج/التحليل", "المناقشة/الاستنتاجات", "اللغة/التنسيق", "أخرى"],
									   # Raw options
									   key="section_raw")
		with col3_form:
			difficulty_val = st.selectbox("سهولة المعالجة:",  # Raw label
										  ["سهلة", "متوسطة", "صعبة"], key="difficulty_raw")  # Raw options

		action_plan = st.text_input("خطة العمل الأولية لهذا التعليق:")  # Raw label
		submitted = st.form_submit_button("إضافة وتصنيف التعليق")  # Raw label

		if submitted and reviewer_comment_text:
			st.session_state.comments_list.append({
				"comment": reviewer_comment_text,
				"importance": importance_val,  # These are already raw Arabic from selectbox
				"section": section_val,
				"difficulty": difficulty_val,
				"action_plan": action_plan
			})
			st.success("تمت إضافة التعليق!")  # Raw

	if st.session_state.comments_list:
		st.markdown("---")
		st.subheader("قائمة التعليقات المصنفة:")  # Raw

		df_comments_classified_raw = pd.DataFrame(st.session_state.comments_list)
		# For DataFrame, pass raw column names. Streamlit should handle display with CSS.
		df_comments_classified_raw.columns = ["التعليق", "الأهمية", "القسم", "سهولة المعالجة", "خطة العمل"]

		st.dataframe(df_comments_classified_raw, use_container_width=True)

		if st.button("مسح قائمة التعليقات"):  # Raw
			st.session_state.comments_list = []
			st.experimental_rerun()

	st.markdown("""
    <div class="tip-box">
        <h3>نصيحة مهمة</h3>
        <p>تذكر أن الهدف النهائي هو تحسين جودة بحثك، وليس مجرد إرضاء المحكمين. استخدم تعليقاتهم كفرصة للتعلم وتطوير مهاراتك البحثية.
        التصنيف المنظم للتعليقات يساعدك على وضع خطة عمل فعالة ومواجهة عملية المراجعة بثقة أكبر.</p>
    </div>
    """, unsafe_allow_html=True)


# صفحة استراتيجيات الرد والتعديل
def response_strategies_page():
	st.title("استراتيجيات الرد على المحكمين وإجراء التعديلات")

	st.markdown("""
    <div class="info-box">
        <p>طريقة ردك على تعليقات المحكمين وكيفية تنفيذ التعديلات المطلوبة تؤثر بشكل كبير على فرص قبول بحثك.
        هذا القسم يقدم استراتيجيات فعالة للرد على المحكمين وإجراء التعديلات بطريقة مقنعة ومنظمة.</p>
    </div>
    """, unsafe_allow_html=True)

	st.subheader("أنواع التعامل مع تعليقات المحكمين ونسبتها")
	df_responses_chart = pd.DataFrame({
		'نوع التعامل': responses_data['نوع التعامل'],  # Raw
		'النسبة': responses_data['النسبة المئوية']
	})
	fig_responses = plot_arabic_pie_plotly(
		df_responses_chart['النسبة'],
		df_responses_chart['نوع التعامل'],  # Pass raw
		"توزيع طرق التعامل مع تعليقات المحكمين",  # Pass raw
		'النسبة',
		'نوع التعامل'
	)
	st.plotly_chart(fig_responses, use_container_width=True)

	st.subheader("مبادئ أساسية للرد على المحكمين")

	st.markdown("""
    <div class="step-box">
        <h4>المبادئ الأساسية لصياغة رد فعال على المحكمين (The Golden Rules):</h4>
        <ol>
            <li><strong><span class="step-number">1</span>الاحترام والمهنية (Be Polite and Professional):</strong> حافظ على لغة مهنية ومحترمة، حتى عند عدم الاتفاق مع التعليقات. اشكر المحكمين على وقتهم وجهدهم.</li>
            <li><strong><span class="step-number">2</span>الشمولية (Be Thorough):</strong> الرد على جميع النقاط المثارة من كل محكم، حتى التعليقات البسيطة أو التي تبدو غير مهمة. لا تتجاهل أي تعليق.</li>
            <li><strong><span class="step-number">3</span>التنظيم (Be Organized):</strong> نظم الرد بشكل منهجي (Point-by-point response). اقتبس تعليق المحكم ثم قدم ردك تحته مباشرة. استخدم ترقيماً واضحاً.</li>
            <li><strong><span class="step-number">4</span>الوضوح (Be Clear):</strong> وضح التغييرات التي أجريتها بدقة، مع الإشارة إلى مواقعها في النسخة المعدلة (رقم الصفحة، الفقرة، السطر، القسم). استخدم تمييزاً للتعديلات في النص (Highlighting or Track Changes).</li>
            <li><strong><span class="step-number">5</span>الدعم العلمي (Be Evidenced-Based):</strong> قدم أدلة وبراهين علمية (من الأدبيات أو من بياناتك) عند الرد على تعليقات أو عند عدم تنفيذ بعض التوصيات.</li>
            <li><strong><span class="step-number">6</span>الإيجاز مع الشمول (Be Concise yet Comprehensive):</strong> الرد بشكل مفصل بما يكفي لتوضيح موقفك وتعديلاتك، دون إطالة غير ضرورية أو تكرار.</li>
            <li><strong><span class="step-number">7</span>الشكر والتقدير (Be Grateful):</strong> ابدأ رسالة الرد بشكر المحرر والمحكمين، واختمها بتجديد الشكر والاستعداد لإجراء تعديلات إضافية.</li>
            <li><strong><span class="step-number">8</span>الإيجابية (Be Positive):</strong> أظهر أنك أخذت التعليقات على محمل الجد وأنك ملتزم بتحسين البحث.</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

	st.subheader("هيكل نموذجي لرسالة الرد على المحكمين")

	with st.expander("عرض هيكل نموذجي لرسالة الرد"):  # Raw
		st.markdown("""
        <div class="example-box">
            <h4>[بداية الرسالة]</h4>
            <blockquote>
                <strong>التاريخ:</strong> [أدخل التاريخ]
                <br>
                <strong>إلى:</strong> محرر مجلة [اسم المجلة]
                <br>
                <strong>من:</strong> [اسمك وأسماء المؤلفين المشاركين]
                <br>
                <strong>الموضوع:</strong> رد على تعليقات المحكمين للبحث رقم [رقم المخطوطة] المعنون: "[عنوان البحث]"
                <br><br>
                السيد/ة المحرر/ة المحترم/ة،
                <br><br>
                نتقدم بخالص الشكر والتقدير لكم وللمحكمين الكرام على الوقت الثمين والجهد المبذول في مراجعة بحثنا. لقد وجدنا تعليقاتكم ومقترحاتكم بناءة وقيمة للغاية، وساعدتنا بشكل كبير في تحسين جودة البحث وعمقه.
                <br><br>
                لقد قمنا بمراجعة جميع التعليقات بعناية وأجرينا التعديلات اللازمة على المخطوطة. نقدم فيما يلي رداً تفصيلياً (نقطة بنقطة) على جميع النقاط المثارة من قبل كل محكم، موضحين التغييرات التي أجريناها في النسخة المعدلة من البحث. تم تمييز التعديلات في النص المرفق (مثلاً، باستخدام خاصية تتبع التغييرات أو بلون مختلف).
            </blockquote>
            <h4>[ملخص التغييرات الرئيسية (اختياري ولكن مفيد)]</h4>
            <blockquote>
                <p>قبل الدخول في الردود التفصيلية، نود تسليط الضوء على أهم التعديلات التي قمنا بها:</p>
                <ol>
                    <li>[التغيير الرئيسي الأول، مثلاً: توسيع العينة وإعادة التحليل الإحصائي...]</li>
                    <li>[التغيير الرئيسي الثاني، مثلاً: تحديث مراجعة الأدبيات وإعادة صياغة الإطار النظري...]</li>
                    <li>[التغيير الرئيسي الثالث، مثلاً: إضافة قسم جديد لمناقشة الآثار التطبيقية...]</li>
                </ol>
            </blockquote>
            <hr>
            <h4>الرد التفصيلي على تعليقات المحكم الأول (Reviewer #1):</h4>
            <blockquote>
                <p><strong>تعليق المحكم 1.1:</strong> "[اقتباس تعليق المحكم الأول هنا بالكامل]"</p>
                <p><strong>ردنا:</strong> نشكر المحكم على هذه الملاحظة المهمة. استجابةً لذلك، قمنا بـ [اشرح التعديل بالتفصيل]. يمكن الاطلاع على هذا التعديل في [حدد الموقع: القسم X، الصفحة Y، الفقرة Z]. نعتقد أن هذا التعديل قد [وضح كيف أدى التعديل لتحسين البحث].</p>
                <p><strong>تعليق المحكم 1.2:</strong> "[اقتباس تعليق المحكم الثاني هنا بالكامل]"</p>
                <p><strong>ردنا:</strong> نقدر هذه الملاحظة القيمة. لقد قمنا بـ [اشرح التعديل أو قدم تبريراً علمياً إذا لم تتفق مع التعليق بالكامل]. التغييرات المتعلقة بهذه النقطة موجودة في [حدد الموقع].</p>
                <p><em>(وهكذا لجميع تعليقات المحكم الأول)</em></p>
            </blockquote>
            <hr>
            <h4>الرد التفصيلي على تعليقات المحكم الثاني (Reviewer #2):</h4>
            <blockquote>
                <p><strong>تعليق المحكم 2.1:</strong> "[اقتباس تعليق المحكم الأول هنا بالكامل]"</p>
                <p><strong>ردنا:</strong> نشكر المحكم على هذا الاقتراح البناء. لقد قمنا بـ [اشرح التعديل]. يمكنكم مراجعة هذا التعديل في [حدد الموقع].</p>
                <p><em>(وهكذا لجميع تعليقات المحكم الثاني، ثم المحكم الثالث إن وجد)</em></p>
            </blockquote>
            <hr>
            <h4>[في حالة وجود تعليقات من المحرر (Editor's Comments)]</h4>
             <blockquote>
                <p><strong>تعليق المحرر 1:</strong> "[اقتباس تعليق المحرر]"</p>
                <p><strong>ردنا:</strong> نشكر السيد المحرر على هذه التوجيهات. لقد أخذنا هذه النقطة في الاعتبار وقمنا بـ [اشرح التعديل].</p>
            </blockquote>
            <hr>
            <h4>الخاتمة:</h4>
            <blockquote>
                نود أن نعبر مجدداً عن شكرنا وامتناننا العميق للمحرر/ة والمحكمين على ملاحظاتهم الثاقبة التي ساهمت بشكل كبير في تحسين جودة هذا البحث. نعتقد أن النسخة المعدلة أصبحت أقوى من الناحية العلمية والمنهجية، وتقدم مساهمة أكثر وضوحاً في مجال الدراسة.
                <br><br>
                نحن على استعداد تام لإجراء أي تعديلات إضافية أو تقديم أي توضيحات قد ترونها ضرورية.
                <br><br>
                مع خالص التقدير والاحترام،
                <br><br>
                [اسم الباحث الرئيسي/المراسل] بالنيابة عن جميع المؤلفين
                <br>
                [الانتماء المؤسسي]
                <br>
                [البريد الإلكتروني]
            </blockquote>
        </div>
        """, unsafe_allow_html=True)

	st.subheader("استراتيجيات التعامل مع أنواع مختلفة من التعليقات")

	with st.expander("رد علمي مدعم بالأدلة (35%)"):  # Raw
		st.markdown("""
        <div class="step-box">
            <h4>التعريف:</h4>
            <p>الرد باستخدام أدلة علمية وبراهين منطقية لتوضيح وجهة نظرك أو دعم قراراتك، خاصة عند عدم الاتفاق (جزئياً أو كلياً) مع بعض تعليقات المحكمين. الهدف ليس الجدال، بل إقناع المحكم والمحرر بأن موقفك له أساس علمي قوي.</p>
            <h4>متى تستخدم هذه الاستراتيجية:</h4>
            <ul>
                <li>عند اختلافك مع المحكم في قضية علمية، منهجية، أو تفسيرية جوهرية.</li>
                <li>عندما تكون هناك تعليقات متناقضة من محكمين مختلفين، وتحتاج لترجيح رأي على آخر.</li>
                <li>عندما لا تستطيع تنفيذ توصية معينة لأسباب علمية، عملية، أو أخلاقية (مع تقديم بدائل إن أمكن).</li>
                <li>عند الحاجة لتبرير استخدام منهجية أو تحليل معين يختلف عما اقترحه المحكم.</li>
            </ul>
            <h4>كيفية تطبيق هذه الاستراتيجية:</h4>
            <ol>
                <li><strong>ابدأ بالاعتراف والتقدير:</strong> اشكر المحكم على تعليقه وأظهر أنك فكرت فيه بعمق (مثال: "نشكر المحكم على هذا الاقتراح المثير للتفكير...").</li>
                <li><strong>وضح وجهة نظرك باحترام:</strong> اشرح لماذا تختلف مع التعليق أو لماذا لا يمكنك تنفيذه بالكامل (مثال: "بينما نتفق مع أهمية النقطة التي أثارها المحكم، نعتقد أن...").</li>
                <li><strong>استشهد بالأدبيات العلمية:</strong> ادعم موقفك بمراجع ودراسات سابقة ذات صلة.</li>
                <li><strong>قدم بيانات أو تحليلات إضافية:</strong> إذا أمكن، قدم أدلة من بياناتك الخاصة لدعم موقفك.</li>
                <li><strong>اشرح المبررات العلمية والمنطقية:</strong> وضح الأساس النظري أو المنهجي لقرارك.</li>
                <li><strong>اعرض البدائل التي نظرت فيها:</strong> اشرح لماذا لم تختر البدائل الأخرى (إن وجدت).</li>
                <li><strong>كن مستعداً للتنازل الجزئي:</strong> إذا أمكن، حاول تلبية جزء من طلب المحكم أو إيجاد حل وسط.</li>
            </ol>
            <h4>مثال:</h4>
            <div class="example-box">
                <p><strong>تعليق المحكم:</strong> "يجب استخدام نموذج الانحدار اللوجستي بدلاً من الانحدار الخطي المتعدد لتحليل البيانات، نظراً لطبيعة المتغير التابع (الذي يبدو فئوياً)."</p>
                <p><strong>الرد (نموذج لرد علمي مدعم بالأدلة):</strong></p>
                <blockquote>
                    "نشكر المحكم على هذه الملاحظة المهمة حول اختيار النموذج الإحصائي المناسب. نقدر اقتراحه باستخدام الانحدار اللوجستي، وقد أخذنا هذا الاقتراح بعين الاعتبار الجاد.
                    <br><br>
                    ومع ذلك، بعد دراسة متأنية لطبيعة متغيرنا التابع ('مستوى الأداء الاقتصادي المقاس على مقياس ليكرت من 1 إلى 7') والتشاور مع الأدبيات المنهجية، قررنا الاستمرار في استخدام نموذج الانحدار الخطي المتعدد (مع بعض التحفظات التي نناقشها الآن في قسم القيود) للأسباب التالية:
                    <br><br>
                    1.  على الرغم من أن مقياس ليكرت هو مقياس ترتيبي، إلا أن هناك نقاشاً واسعاً في الأدبيات (e.g., Norman, 2010; Sullivan & Artino, 2013) حول جواز استخدام الاختبارات البارامترية مع بيانات ليكرت، خاصة عندما يكون عدد الفئات 5 أو أكثر ويُفترض أن المسافات بين الفئات متساوية تقريباً، وهو ما نراه متوفراً في حالتنا.
                    <br><br>
                    2.  استخدام الانحدار الخطي يسمح بتفسير مباشر أكثر للمعاملات (Coefficients) من حيث التغير في المتوسط، وهو ما يتناسب مع أسئلة بحثنا.
                    <br><br>
                    3.  قمنا بالتحقق من افتراضات نموذج الانحدار الخطي، بما في ذلك التوزيع الطبيعي للبواقي (Residuals) وتجانس التباين (Homoscedasticity)، ووجدنا أنها متحققة بشكل مقبول (انظر الملحق B، الأشكال B1 و B2، ص 25-26).
                    <br><br>
                    4.  لضمان متانة النتائج، وكاستجابة جزئية لتعليق المحكم، قمنا بإجراء تحليل حساسية باستخدام نموذج الانحدار الرتبي (Ordinal Logistic Regression) كنموذج بديل. ووجدنا أن النتائج الرئيسية (من حيث اتجاه وأهمية المعاملات) متسقة عبر النموذجين (انظر الجدول 5 الجديد، ص 16).
                    <br><br>
                    ومع ذلك، تقديراً لملاحظة المحكم، أضفنا الآن مناقشة أكثر تفصيلاً لهذه الخيارات المنهجية في قسم المنهجية (ص 10) وقسم القيود (ص 19)، وأوضحنا أن تفسير النتائج يجب أن يأخذ طبيعة المتغير التابع في الاعتبار. كما اقترحنا استخدام نماذج إحصائية بديلة في الدراسات المستقبلية لمزيد من التحقق."
                </blockquote>
            </div>
        </div>
        """, unsafe_allow_html=True)
	# ... (Repeat for other expanders, using raw Arabic strings for titles) ...
	with st.expander("قبول التعليق مع تعديل (30%)"):
		st.markdown("""
        <div class="step-box">
            <h4>التعريف:</h4>
            <p>قبول تعليق المحكم والقيام بالتعديلات المطلوبة بشكل كامل، مع توضيح كيفية تنفيذ التعديل وأين تم ذلك في النسخة المعدلة.</p>
            <h4>متى تستخدم هذه الاستراتيجية:</h4>
            <ul>
                <li>عندما تتفق مع تعليق المحكم وترى قيمته في تحسين البحث</li>
                <li>عندما يشير أكثر من محكم إلى نفس المشكلة</li>
                <li>عندما يتعلق التعليق بمشكلة واضحة في البحث</li>
                <li>عندما يكون التعديل المطلوب ممكناً من الناحية العملية</li>
            </ul>
            <h4>كيفية تطبيق هذه الاستراتيجية:</h4>
            <ol>
                <li>اشكر المحكم على الملاحظة</li>
                <li>أظهر اتفاقك مع التعليق وأهميته</li>
                <li>صف بوضوح التعديلات التي أجريتها</li>
                <li>حدد المواقع الدقيقة للتغييرات في النسخة المعدلة</li>
                <li>وضح كيف ساهمت هذه التعديلات في تحسين البحث</li>
            </ol>
            <h4>مثال:</h4>
            <div class="example-box">
                <p><strong>تعليق المحكم:</strong> "مراجعة الأدبيات غير محدثة وتفتقر للدراسات الحديثة خاصة بعد عام 2020، رغم أن هناك تطورات مهمة في هذا المجال خلال السنوات الأخيرة."</p>
                <p><strong>الرد (نموذج لقبول التعليق مع تعديل):</strong></p>
                <blockquote>
                    "نشكر المحكم على هذه الملاحظة المهمة والدقيقة. نتفق تماماً مع أن مراجعة الأدبيات في النسخة السابقة كانت تفتقر للدراسات الحديثة، وقد قمنا بتحديثها بشكل شامل على النحو التالي:
                    <br><br>
                    1. أضفنا 14 دراسة حديثة نُشرت بين عامي 2020-2025 (انظر المراجع الجديدة أرقام 27-40 في قائمة المراجع).
                    <br><br>
                    2. أضفنا قسماً فرعياً جديداً بعنوان "التطورات الحديثة في نظريات التسعير الديناميكي" (القسم 2.3، الصفحات 6-7) يلخص أحدث الاتجاهات النظرية في المجال.             
                    <br><br>
                    3. أعدنا تنظيم مراجعة الأدبيات بشكل موضوعي بدلاً من السرد الزمني، لتسهيل الربط بين الدراسات المختلفة وإبراز التطور في المفاهيم والمنهجيات.
                    <br><br>
                    4. أضفنا جدولاً تلخيصياً (الجدول 1، صفحة 5) يعرض الدراسات الرئيسية في المجال منذ عام 2018، مع تحديد منهجياتها ونتائجها الرئيسية والفجوات البحثية التي حددتها.
                    <br><br>
                    5. عدّلنا صياغة الفجوة البحثية في نهاية مراجعة الأدبيات (صفحة 8) لتعكس المعرفة الحالية في ضوء الدراسات الحديثة.
                    <br><br>
                    نعتقد أن هذه التعديلات قد ساهمت في تقوية الأساس النظري للبحث وتوضيح مساهمته الفريدة في ضوء الأدبيات الحديثة. نشكر المحكم مرة أخرى على هذه الملاحظة القيمة التي ساعدتنا في تحسين جودة البحث بشكل كبير."
                </blockquote>
            </div>
        </div>
        """, unsafe_allow_html=True)

	with st.expander("توضيح سوء فهم (20%)"):
		st.markdown("""
        <div class="step-box">
            <h4>التعريف:</h4>
            <p>توضيح نقطة قد أساء المحكم فهمها في البحث، مع تحسين طريقة عرضها في النسخة المعدلة لتجنب سوء الفهم مستقبلاً.</p>
            <h4>متى تستخدم هذه الاستراتيجية:</h4>
            <ul>
                <li>عندما يكون تعليق المحكم مبنياً على فهم غير دقيق لما ورد في البحث</li>
                <li>عندما تكون المعلومات موجودة بالفعل في البحث ولكن ربما بشكل غير واضح</li>
                <li>عندما يكون هناك سوء فهم لمصطلح أو مفهوم استخدمته في البحث</li>
                <li>عندما يطلب المحكم معلومات سبق تقديمها في البحث</li>
            </ul>
            <h4>كيفية تطبيق هذه الاستراتيجية:</h4>
            <ol>
                <li>تجنب استخدام عبارات مثل "المحكم أخطأ" أو "المحكم لم يفهم"</li>
                <li>ابدأ بالاعتراف بأن العرض قد لا يكون واضحاً بما فيه الكفاية</li>
                <li>وضح النقطة محل سوء الفهم بشكل مباشر وبسيط</li>
                <li>اشرح كيف قمت بتحسين العرض في النسخة المعدلة لتجنب سوء الفهم</li>
                <li>قدم إشارات دقيقة لمواقع المعلومات في النسخة الأصلية والمعدلة</li>
            </ol>
            <h4>مثال:</h4>
            <div class="example-box">
                <p><strong>تعليق المحكم:</strong> "الباحثون لم يوضحوا كيفية التعامل مع البيانات المفقودة، مما يثير تساؤلات حول دقة النتائج."</p>
                <p><strong>الرد (نموذج لتوضيح سوء فهم):</strong></p>
                <blockquote>
                    "نشكر المحكم على هذه الملاحظة المهمة حول البيانات المفقودة. ندرك أن طريقة التعامل مع البيانات المفقودة تؤثر بشكل كبير على دقة النتائج. وقد قمنا بالفعل بتوضيح منهجيتنا في التعامل مع البيانات المفقودة في النسخة السابقة (القسم 3.4، صفحة 11، الفقرة الثانية)، حيث ذكرنا استخدام طريقة الإسناد المتعدد (Multiple Imputation) لمعالجة القيم المفقودة في المتغيرات المستقلة، والتي كانت نسبتها منخفضة (أقل من 5%).
                    <br><br>
                    ومع ذلك، نتفهم أن هذه المعلومات قد لا تكون موضحة بشكل كافٍ في النسخة السابقة. لذلك، قمنا بتحسين وتوسيع شرح منهجية التعامل مع البيانات المفقودة في النسخة المعدلة على النحو التالي:
                    <br><br>
                    1. أضفنا قسماً فرعياً مستقلاً بعنوان "التعامل مع البيانات المفقودة" (القسم 3.4.2، صفحة 12-13).
                    <br><br>
                    2. قدمنا جدولاً يوضح نسبة البيانات المفقودة لكل متغير (الجدول 3، صفحة 12).
                    <br><br>
                    3. شرحنا بالتفصيل أسباب اختيار طريقة الإسناد المتعدد بدلاً من الطرق البديلة مثل حذف الحالات أو استبدال القيم المفقودة بالمتوسط.
                    <br><br>
                    4. أضفنا تحليل حساسية (sensitivity analysis) في الملحق C (صفحة 28) لاختبار تأثير طرق مختلفة للتعامل مع البيانات المفقودة على النتائج الرئيسية.
                    <br><br>
                    نأمل أن تكون هذه التوضيحات والإضافات كافية لإزالة أي غموض حول منهجيتنا في التعامل مع البيانات المفقودة وتأثيرها على النتائج."
                </blockquote>
            </div>
        </div>
        """, unsafe_allow_html=True)

	with st.expander("تقديم تحليل إضافي (10%)"):
		st.markdown("""
        <div class="step-box">
            <h4>التعريف:</h4>
            <p>إجراء تحليلات إضافية أو تقديم بيانات إضافية استجابةً لتعليقات المحكمين، لتعزيز النتائج أو اختبار فرضيات بديلة.</p>
            <h4>متى تستخدم هذه الاستراتيجية:</h4>
            <ul>
                <li>عندما يطلب المحكم تحليلات إضافية لتقوية النتائج</li>
                <li>عندما يشكك المحكم في متانة النتائج أو قابليتها للتعميم</li>
                <li>عندما يقترح المحكم متغيرات أو علاقات إضافية تستحق الدراسة</li>
                <li>عندما تحتاج لاختبار فرضيات بديلة أثارها المحكم</li>
            </ul>
            <h4>كيفية تطبيق هذه الاستراتيجية:</h4>
            <ol>
                <li>وضح الغرض من التحليل الإضافي وكيف يرتبط بتعليق المحكم</li>
                <li>اشرح منهجية التحليل الإضافي بشكل مختصر</li>
                <li>قدم النتائج الرئيسية للتحليل الإضافي</li>
                <li>وضح كيف تدعم هذه النتائج الإضافية (أو تعدل) استنتاجات البحث الأصلية</li>
                <li>ضع التفاصيل الفنية للتحليل في الملاحق إذا كانت مطولة</li>
            </ol>
            <h4>مثال:</h4>
            <div class="example-box">
                <p><strong>تعليق المحكم:</strong> "لم يقم الباحثون باختبار تأثير متغير حجم الشركة كمتغير معدل للعلاقة بين الاستثمار في التكنولوجيا والأداء المالي، رغم أن الأدبيات تشير إلى أهمية هذا المتغير."</p>
                <p><strong>الرد (نموذج لتقديم تحليل إضافي):</strong></p>
                <blockquote>
                    "نشكر المحكم على هذه الملاحظة القيمة حول الدور المحتمل لحجم الشركة كمتغير معدل. نتفق مع المحكم أن الأدبيات السابقة (مثل دراسات Wang et al., 2019; AlSharif, 2022) تشير إلى أهمية هذا المتغير في العلاقة بين الاستثمار التكنولوجي والأداء المالي.
                    <br><br>
                    استجابةً لهذا التعليق، قمنا بإجراء تحليل إضافي لاختبار الدور المعدل لحجم الشركة. على وجه التحديد:
                    <br><br>
                    1. قمنا بتقسيم عينة الدراسة إلى ثلاث فئات بناءً على حجم الشركة (صغيرة، متوسطة، كبيرة) باستخدام إجمالي الأصول كمؤشر للحجم.
                    <br><br>
                    2. أجرينا تحليل الانحدار لكل فئة على حدة لاختبار ما إذا كانت العلاقة بين الاستثمار التكنولوجي والأداء المالي تختلف باختلاف حجم الشركة.
                    <br><br>
                    3. أضفنا متغير تفاعلي (الاستثمار التكنولوجي × حجم الشركة) في نموذج الانحدار الأساسي لاختبار الأثر المعدل بشكل مباشر.
                    <br><br>
                    نتائج هذا التحليل الإضافي (المعروضة في الجدول 6 الجديد، صفحة 17) كشفت عن وجود أثر معدل دال إحصائياً لحجم الشركة، حيث كانت العلاقة بين الاستثمار التكنولوجي والأداء المالي أقوى في الشركات الكبيرة مقارنة بالشركات الصغيرة والمتوسطة. هذه النتيجة تتسق مع نظرية وفورات الحجم وتضيف نظرة أكثر دقة للعلاقة الرئيسية المدروسة في البحث.
                    <br><br>
                    بناءً على هذه النتائج، قمنا بتعديل مناقشة النتائج (القسم 6.2، صفحة 19) والاستنتاجات (القسم 7.1، صفحة 21) لتعكس هذا البعد الإضافي. كما أضفنا توصية للشركات الصغيرة والمتوسطة حول كيفية تعظيم العائد من استثماراتها التكنولوجية في ظل هذه النتائج (القسم 7.2، صفحة 22).
                    <br><br>
                    نعتقد أن هذا التحليل الإضافي قد أثرى البحث وعزز من قيمته العلمية والتطبيقية، ونشكر المحكم على اقتراحه القيم."
                </blockquote>
            </div>
        </div>
        """, unsafe_allow_html=True)

	with st.expander("الاعتراف بالقيود (5%)"):
		st.markdown("""
        <div class="step-box">
            <h4>التعريف:</h4>
            <p>الاعتراف بصحة ملاحظة المحكم وقبولها كقيد من قيود البحث عندما لا يمكن معالجتها بشكل كامل، مع توضيح آثارها على البحث واقتراح سبل معالجتها في دراسات مستقبلية.</p>
            <h4>متى تستخدم هذه الاستراتيجية:</h4>
            <ul>
                <li>عندما تكون ملاحظة المحكم صحيحة ولكن لا يمكن معالجتها بالكامل (مثلاً، لقيود في البيانات)</li>
                <li>عندما تتطلب المعالجة إعادة تصميم البحث بشكل كامل</li>
                <li>عندما تشير الملاحظة إلى حدود منهجية أو نظرية لا يمكن تجاوزها في إطار البحث الحالي</li>
                <li>عندما تكون المعالجة الكاملة خارج نطاق البحث الحالي</li>
            </ul>
            <h4>كيفية تطبيق هذه الاستراتيجية:</h4>
            <ol>
                <li>اعترف بصحة ملاحظة المحكم وأهميتها</li>
                <li>وضح سبب عدم إمكانية معالجتها بشكل كامل في البحث الحالي</li>
                <li>ناقش الآثار المحتملة لهذا القيد على نتائج البحث</li>
                <li>أضف هذا القيد بوضوح في قسم قيود البحث</li>
                <li>اقترح كيفية معالجة هذا القيد في البحوث المستقبلية</li>
                <li>إذا أمكن، قم ببعض التعديلات الجزئية لتخفيف آثار هذا القيد</li>
            </ol>
            <h4>مثال:</h4>
            <div class="example-box">
                <p><strong>تعليق المحكم:</strong> "البحث يعتمد على بيانات مقطعية (cross-sectional) وبالتالي لا يمكنه إثبات العلاقات السببية بين المتغيرات، رغم أن الباحثين يستخدمون لغة توحي بالسببية في الاستنتاجات."</p>
                <p><strong>الرد (نموذج للاعتراف بالقيود):</strong></p>
                <blockquote>
                    "نشكر المحكم على هذه الملاحظة المهمة والدقيقة حول محدودية البيانات المقطعية في إثبات العلاقات السببية. نتفق تماماً مع هذه الملاحظة ونعترف بأنها تمثل قيداً مهماً للبحث الحالي.
                    <br><br>
                    في الواقع، يستند تصميم بحثنا إلى بيانات مقطعية تم جمعها في نقطة زمنية واحدة، وهذا يحد من قدرتنا على استنتاج علاقات سببية قاطعة بين الاستثمار التكنولوجي والأداء المالي للشركات. استجابةً لهذه الملاحظة، قمنا بما يلي:
                    <br><br>
                    1. مراجعة صياغة الاستنتاجات في جميع أنحاء البحث لاستبدال العبارات التي توحي بالسببية (مثل "يؤدي إلى"، "يسبب"، "ينتج عنه") بعبارات أكثر دقة تعكس طبيعة العلاقة الارتباطية (مثل "يرتبط بـ"، "يتوافق مع"، "تظهر علاقة بين").
                    <br><br>
                    2. إضافة قسم فرعي جديد في قسم قيود البحث (القسم 7.3.1، صفحة 23) يناقش بوضوح محدودية البيانات المقطعية وآثارها على تفسير النتائج.
                    <br><br>
                    3. اقتراح تصميم طولي (longitudinal) في توصيات البحوث المستقبلية (القسم 7.4، صفحة 24) لدراسة العلاقة السببية بشكل أفضل، من خلال جمع بيانات على مدى فترات زمنية متعددة.
                    <br><br>
                    4. إجراء تحليل إضافي للمتغيرات الوسيطة المحتملة (الملحق D، صفحة 30) لتقديم فهم أعمق للعلاقات، مع الاعتراف بأن هذا لا يعوض تماماً عن التصميم الطولي.
                    <br><br>
                    نعتقد أن هذه التعديلات تعالج بشكل صريح القيد المذكور وتساعد القراء على تفسير النتائج بشكل أكثر دقة. ومع ذلك، نعترف بأن المعالجة الكاملة لهذا القيد تتطلب تصميماً بحثياً مختلفاً، وهو ما نقترحه للبحوث المستقبلية."
                </blockquote>
            </div>
        </div>
        """, unsafe_allow_html=True)

	st.subheader("نصائح عامة للتعامل مع تعليقات المحكمين")
	col1_tips, col2_tips = st.columns(2)

	with col1_tips:
		st.markdown("""
        <div class="card" style="background-color: #e7f3fe;">
            <h4><span class="step-number">💡</span> قبل البدء في الرد</h4>
            <ul>
                <li>خذ وقتاً كافياً (يوم أو يومين) لاستيعاب التعليقات واحتواء المشاعر السلبية الأولية. لا ترد وأنت غاضب!</li>
                <li>اقرأ التعليقات عدة مرات (مرة للقراءة السريعة، مرة للفهم العميق، مرة لوضع خطة).</li>
                <li>صنف التعليقات (باستخدام جدول مثلاً) حسب أهميتها، طبيعتها، والمحكم لتحديد أولويات العمل.</li>
                <li>ناقش التعليقات مع المشاركين في البحث أو مع زملاء خبراء وموثوقين للحصول على وجهة نظر أخرى.</li>
                <li>ضع خطة عمل واضحة ومنظمة للتعديلات، مع جدول زمني تقديري لكل مهمة.</li>
            </ul>
        </div>

        <div class="card" style="background-color: #fff0f0; margin-top: 15px;">
            <h4><span class="step-number">🚫</span> أخطاء يجب تجنبها</h4>
            <ul>
                <li>تجاهل بعض التعليقات دون تقديم مبررات واضحة.</li>
                <li>الرد بطريقة دفاعية، هجومية، أو غير محترمة (تذكر أن المحرر يقرأ الرد).</li>
                <li>إجراء تعديلات سطحية لا تعالج جوهر المشكلة التي أشار إليها المحكم.</li>
                <li>الإفراط في الوعود التي لا يمكن تحقيقها ضمن الوقت أو الموارد المتاحة.</li>
                <li>التأخر في الرد وتجاوز المدة المحددة من المجلة دون طلب تمديد مبرر.</li>
                <li>كتابة رد مختصر جداً لا يشرح التعديلات بشكل كافٍ، أو رد طويل جداً وممل.</li>
                <li>إلقاء اللوم على المحكمين أو التشكيك في خبرتهم.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

	with col2_tips:
		st.markdown("""
        <div class="card" style="background-color: #f0fff5;">
            <h4><span class="step-number">✍️</span> نصائح لكتابة رد فعال</h4>
            <ul>
                <li>استخدم لغة مهنية، إيجابية، ومحترمة دائماً.</li>
                <li>نظم ردك بنفس ترتيب تعليقات المحكمين (م1: ت1، ت2... ثم م2: ت1، ت2...) لسهولة المتابعة.</li>
                <li>استخدم ترقيماً واضحاً وتنسيقاً (خطوط، مسافات) يسهل قراءة الرد.</li>
                <li>حدد مواقع التغييرات في النسخة المعدلة بدقة (رقم الصفحة، الفقرة، القسم، الجدول، الشكل).</li>
                <li>اقتبس تعليق المحكم بالكامل قبل الرد عليه (لتوفير وقته في الرجوع للتقرير الأصلي).</li>
                <li>ابدأ ردك على كل تعليق بالشكر والإشادة بقيمة التعليق (حتى لو لم تتفق معه).</li>
                <li>قدم أدلة علمية ومبررات منطقية عند الاختلاف مع بعض التعليقات أو عدم تنفيذها بالكامل.</li>
            </ul>
        </div>

        <div class="card" style="background-color: #f5f0ff; margin-top: 15px;">
            <h4><span class="step-number">⚠️</span> التعامل مع المواقف الصعبة</h4>
            <ul>
                <li><strong>تعليقات متناقضة:</strong> اشرح للمحرر كيف حاولت التوفيق بينها، أو لماذا فضلت رأياً على آخر مع تقديم مبرراتك.</li>
                <li><strong>تعليقات غير واضحة أو غامضة:</strong> حاول تفسيرها بأفضل ما يمكن، وإذا تعذر ذلك، اطلب توضيحاً من المحرر بلباقة أو وضح فهمك لها وكيف رددت بناءً عليه.</li>
                <li><strong>تعليقات خارج نطاق البحث:</strong> اشرح بلطف لماذا تعتبرها خارج النطاق الحالي للبحث، واقترحها للدراسات المستقبلية.</li>
                <li><strong>تعليقات تتطلب موارد غير متاحة (وقت، مال، بيانات):</strong> كن صريحاً بشأن القيود، واقترح بدائل عملية أو تعديلات جزئية.</li>
                <li><strong>تعليقات تبدو شخصية أو غير موضوعية:</strong> ركز على الجوانب العلمية فقط في ردك وتجنب الرد بالمثل. المحرر سيلاحظ ذلك.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

	st.subheader("الأسئلة الشائعة حول التعامل مع تعليقات المحكمين")
	with st.expander("ما هي المدة المناسبة للرد على تعليقات المحكمين؟"):  # Raw
		st.markdown("""
        <div class="step-box">
            <p>تختلف المدة المناسبة للرد حسب حجم التعديلات المطلوبة وطبيعتها:</p>
            <ul>
                <li><strong>تعديلات طفيفة:</strong> 2-4 أسابيع</li>
                <li><strong>تعديلات رئيسية:</strong> 1-3 أشهر</li>
                <li><strong>إعادة تقديم بعد رفض:</strong> 3-6 أشهر</li>
            </ul>
            <p>نصائح إضافية:</p>
            <ul>
                <li>التزم بالموعد النهائي الذي تحدده المجلة إن وجد</li>
                <li>إذا كنت بحاجة لوقت إضافي، اطلب تمديداً من المحرر مع شرح الأسباب</li>
                <li>لا تتسرع في الرد على حساب جودة التعديلات</li>
                <li>خصص وقتاً كافياً لمراجعة النسخة المعدلة قبل إعادة تقديمها</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
	# ... (Repeat for other FAQs on this page, using raw Arabic strings for titles) ...
	with st.expander("كيف أتعامل مع تعليق أعتقد أنه غير عادل أو غير صحيح علمياً؟"):
		st.markdown("""
        <div class="step-box">
            <p>التعامل مع تعليقات تعتقد أنها غير عادلة أو غير صحيحة يتطلب حذراً ودبلوماسية:</p>
            <ol>
                <li><strong>أعد قراءة التعليق بموضوعية:</strong> تأكد من فهمك الصحيح له وابحث عن وجهة نظر المحكم</li>
                <li><strong>استشر زملاء محايدين:</strong> اطلب رأي زملاء لم يشاركوا في البحث لتقييم التعليق بموضوعية</li>
                <li><strong>استخدم "الرد العلمي المدعم بالأدلة":</strong> قدم حجة علمية مدعمة بالأدبيات والأدلة</li>
                <li><strong>تجنب اللغة الدفاعية:</strong> لا تستخدم عبارات مثل "المحكم مخطئ" أو "هذا التعليق غير منصف"</li>
                <li><strong>ابدأ بنقاط الاتفاق:</strong> اعترف بالجوانب الصحيحة في التعليق قبل توضيح وجهة نظرك المختلفة</li>
                <li><strong>قدم بدائل:</strong> اقترح حلولاً وسطية أو مقاربات بديلة تراعي مخاوف المحكم</li>
                <li><strong>في الحالات القصوى:</strong> يمكن مخاطبة المحرر بشكل منفصل لتوضيح موقفك، مع الحفاظ على المهنية والاحترام</li>
            </ol>
            <div class="example-box">
                <p><strong>مثال لرد على تعليق تعتقد أنه غير دقيق علمياً:</strong></p>
                <blockquote>
                    "نشكر المحكم على اهتمامه بهذه النقطة المهمة. يشير المحكم إلى أن 'نموذج X غير مناسب للبيانات غير الخطية، ويجب استخدام نموذج Y بدلاً منه'. نتفق مع المحكم على أهمية اختيار النموذج المناسب لطبيعة البيانات.
                    <br><br>
                    ومع ذلك، تشير الأدبيات الحديثة في هذا المجال (مثل دراسات Johnson et al., 2023; Al-Qahtani, 2024) إلى أن نموذج X يمكن استخدامه بكفاءة مع البيانات غير الخطية عند إضافة مكونات تحويلية محددة، وهو النهج الذي اتبعناه في بحثنا.
                    <br><br>
                    لتوضيح هذه النقطة، أضفنا قسماً في المنهجية (ص 9) يشرح بالتفصيل كيف قمنا بتعديل نموذج X للتعامل مع عدم الخطية في البيانات، مع إشارات للأدبيات ذات الصلة. كما أضفنا تحليلاً للبواقي (Residual Analysis) في الملحق B للتحقق من ملاءمة النموذج.
                    <br><br>
                    بالإضافة إلى ذلك، قمنا بإجراء تحليل حساسية (ص 16) يقارن بين نتائج نموذجنا المعدل ونموذج Y المقترح من المحكم، ووجدنا تقارباً كبيراً في النتائج، مما يدعم سلامة منهجيتنا."
                </blockquote>
            </div>
        </div>
        """, unsafe_allow_html=True)

	with st.expander("هل يجب علي تنفيذ جميع تعديلات المحكمين، حتى التي لا أتفق معها؟"):
		st.markdown("""
        <div class="step-box">
            <p>ليس بالضرورة تنفيذ كل التعديلات حرفياً، لكن يجب التعامل مع كل تعليق بجدية:</p>
            <h4>إرشادات عامة:</h4>
            <ul>
                <li><strong>تعليقات حاسمة متفق عليها من المحكمين:</strong> ينبغي تنفيذها بالكامل</li>
                <li><strong>تعليقات مهمة لكن لا تتفق معها علمياً:</strong> يمكن تقديم رد علمي مدعم بالأدلة</li>
                <li><strong>تعليقات غير ممكنة التنفيذ عملياً:</strong> اشرح القيود وقدم بدائل أو حلولاً جزئية</li>
                <li><strong>تعليقات متناقضة بين المحكمين:</strong> اختر الأنسب منها مع تبرير اختيارك</li>
                <li><strong>تعليقات خارج نطاق البحث:</strong> يمكن توضيح سبب اعتبارها خارج النطاق واقتراحها للدراسات المستقبلية</li>
            </ul>
            <h4>نصائح مهمة:</h4>
            <ol>
                <li>تعامل مع كل تعليق، حتى لو لم تنفذه بالكامل</li>
                <li>قدم مبررات علمية وموضوعية عند عدم تنفيذ تعليق ما</li>
                <li>إذا كان المحرر قد أشار إلى تعليقات معينة كأولوية، فركز عليها</li>
                <li>حاول تحقيق توازن بين رؤيتك البحثية واحترام تعليقات المحكمين</li>
                <li>تذكر أن الهدف النهائي هو تحسين البحث وليس مجرد إرضاء المحكمين</li>
            </ol>
            <div class="example-box">
                <p><strong>مثال لتعامل متوازن مع تعليق لا تتفق معه تماماً:</strong></p>
                <blockquote>
                    "نشكر المحكم على اقتراحه بإضافة فصل كامل لمناقشة الجوانب القانونية للظاهرة المدروسة. نقدر أهمية هذا الجانب، ومع ذلك نرى أن إضافة فصل كامل قد يغير من تركيز البحث الأساسي الذي يستهدف الجوانب الاقتصادية بشكل رئيسي.
                    <br><br>
                    كحل وسط، قمنا بإضافة قسم فرعي جديد (القسم 4.3، ص 12-13) يناقش بإيجاز أهم الجوانب القانونية ذات الصلة المباشرة بموضوع البحث، مع التركيز على تأثيراتها الاقتصادية. كما أشرنا في قسم الدراسات المستقبلية (ص 22) إلى أهمية إجراء دراسات متخصصة تتناول التفاعل بين الجوانب القانونية والاقتصادية للظاهرة بشكل أكثر تفصيلاً.
                    <br><br>
                    نأمل أن يكون هذا التعديل متوازناً بين الحفاظ على تركيز البحث وتناول الجانب القانوني المهم الذي أشار إليه المحكم."
                </blockquote>
            </div>
        </div>
        """, unsafe_allow_html=True)

	st.markdown("""
    <div class="tip-box">
        <h3>نصيحة ختامية</h3>
        <p>تذكر دائماً أن عملية التحكيم والمراجعة، رغم صعوبتها أحياناً، تهدف في النهاية إلى تحسين جودة البحث العلمي.
        التعامل الإيجابي والمهني مع تعليقات المحكمين يساعد في تطوير البحث وتعزيز مهاراتك كباحث، ويزيد من فرص قبول بحثك للنشر.</p>
    </div>
    """, unsafe_allow_html=True)


# صفحة الأسئلة الشائعة (العامة)
def faq_page():
	st.title("الأسئلة الشائعة حول رفض المقالات في المجلات الاقتصادية")  # Raw

	st.markdown("""
    <div class="info-box">
        <p>في هذا القسم، نجيب على أكثر الأسئلة شيوعاً حول رفض المقالات في المجلات الاقتصادية وكيفية التعامل معها بشكل عام.</p>
    </div>
    """, unsafe_allow_html=True)

	with st.expander("ما هي نسبة رفض المقالات في المجلات الاقتصادية عالية التأثير؟"):  # Raw
		st.markdown("""
        <div class="step-box">
            <p>تختلف نسب الرفض بين المجلات، ولكن بشكل عام:</p>
            <ul>
                <li><strong>المجلات الاقتصادية في الفئة Q1 (أعلى 25%):</strong> نسبة الرفض تتراوح بين 85-95%</li>
                <li><strong>المجلات الاقتصادية في الفئة Q2:</strong> نسبة الرفض تتراوح بين 70-85%</li>
                <li><strong>المجلات الاقتصادية في الفئة Q3 و Q4:</strong> نسبة الرفض تتراوح بين 40-70%</li>
            </ul>
            <p>أمثلة لنسب الرفض في بعض المجلات الاقتصادية البارزة (تقريبية):</p>
            <ul>
                <li>American Economic Review: 93-95%</li>
                <li>Journal of Finance: 90-93%</li>
                <li>Quarterly Journal of Economics: 95-97%</li>
                <li>Journal of Economic Literature: 88-92%</li>
                <li>Economic Journal: 85-90%</li>
            </ul>
            <p>من المهم ملاحظة أن نسبة كبيرة من المقالات المرفوضة (40-50%) يتم رفضها في مرحلة مبكرة (Desk Rejection) دون إرسالها للتحكيم، خاصة في المجلات عالية التأثير.</p>
        </div>
        """, unsafe_allow_html=True)
	# ... (Repeat for other FAQs, using raw Arabic strings for titles) ...
	with st.expander("هل يمكن الاستئناف ضد قرار الرفض؟"):
		st.markdown("""
        <div class="step-box">
            <p>نعم، يمكن في بعض الحالات الاستئناف ضد قرار الرفض، ولكن هناك عدة اعتبارات مهمة:</p>
            <h4>متى يمكن التفكير في الاستئناف:</h4>
            <ul>
                <li>وجود أخطاء واضحة في فهم المحكمين للبحث</li>
                <li>وجود تحيز واضح أو غير موضوعي في تقييم المحكمين</li>
                <li>تناقض شديد بين تقييمات المحكمين دون ترجيح واضح من المحرر</li>
                <li>ظهور أدلة جديدة ومهمة تدعم نتائج البحث بعد تقديمه</li>
                <li>وجود سوء فهم جوهري من المحرر لموضوع البحث</li>
            </ul>
            <h4>كيفية تقديم الاستئناف:</h4>
            <ol>
                <li>تحقق من سياسة المجلة بخصوص الاستئناف قبل الشروع فيه</li>
                <li>وجه رسالة مهنية ومحترمة إلى المحرر الرئيسي</li>
                <li>قدم أسباباً محددة وموضوعية للاستئناف، مدعومة بالأدلة</li>
                <li>تجنب اللغة العاطفية أو الدفاعية</li>
                <li>كن واقعياً في توقعاتك؛ فمعظم قرارات الاستئناف تأتي مؤيدة للقرار الأصلي</li>
            </ol>
            <h4>نموذج مختصر لرسالة استئناف:</h4>
            <div class="example-box">
                <p>السيد المحرر الرئيسي المحترم،</p>
                <p>أكتب إليكم بخصوص بحثنا المعنون "عنوان البحث" (رقم التقديم: XXXX) الذي تم رفضه في [التاريخ].</p>
                <p>بعد دراسة متأنية لتقارير المحكمين وقرار الرفض، نود أن نطلب بكل احترام إعادة النظر في هذا القرار للأسباب التالية:</p>
                <ol>
                    <li>يبدو أن المحكم الثاني أساء فهم المنهجية المستخدمة في البحث، حيث أشار إلى أننا استخدمنا [X] بينما المنهجية الفعلية كانت [Y] كما هو موضح بالتفصيل في القسم 3.2 من البحث.</li>
                    <li>اعتمد قرار الرفض بشكل أساسي على تقرير المحكم الثالث، بينما كان تقييم المحكمين الأول والثاني إيجابياً بشكل عام، مما يثير تساؤلات حول الترجيح المعطى لكل تقرير.</li>
                </ol>
                <p>نحن على استعداد لإجراء التعديلات اللازمة لمعالجة المخاوف الحقيقية التي أثارها المحكمون، ونعتقد أن البحث يقدم مساهمة مهمة في المجال تستحق النشر في مجلتكم المرموقة.</p>
                <p>نقدر وقتكم واهتمامكم بإعادة النظر في قرار الرفض.</p>
                <p>مع خالص التقدير،</p>
                <p>اسم الباحث</p>
            </div>
            <h4>نصائح مهمة:</h4>
            <ul>
                <li>احتمالية نجاح الاستئناف منخفضة عموماً (أقل من 10-15%)</li>
                <li>فكر ملياً قبل تقديم الاستئناف، وقيّم موضوعية أسبابك</li>
                <li>استشر زملاء ذوي خبرة قبل اتخاذ قرار الاستئناف</li>
                <li>في معظم الحالات، قد يكون من الأفضل تحسين البحث وتقديمه لمجلة أخرى</li>
                <li>لا تقدم استئنافاً ضد الرفض المباشر (Desk Rejection) إلا في حالات استثنائية جداً</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

	with st.expander("ما هي المدة المناسبة لإعادة تقديم البحث بعد الرفض؟"):
		st.markdown("""
        <div class="step-box">
            <p>تعتمد المدة المناسبة لإعادة تقديم البحث بعد الرفض على عدة عوامل:</p>
            <h4>العوامل المؤثرة في تحديد المدة:</h4>
            <ul>
                <li>حجم وطبيعة التعديلات المطلوبة</li>
                <li>نوع الرفض (مباشر، بعد التحكيم، مع إمكانية إعادة التقديم)</li>
                <li>الحاجة لجمع بيانات إضافية أو إجراء تحليلات جديدة</li>
                <li>عدد وتوفر المشاركين في البحث</li>
                <li>الموعد النهائي المحدد من المجلة (إن وجد)</li>
            </ul>
            <h4>إرشادات عامة للمدة المناسبة:</h4>
            <ul>
                <li><strong>رفض مباشر (Desk Rejection):</strong>
                    <ul>
                        <li>إعادة التقديم لمجلة أخرى: 2-4 أسابيع</li>
                        <li>(التعديلات هنا غالباً تتعلق بملاءمة البحث للمجلة الجديدة وتنسيقه وفق متطلباتها)</li>
                    </ul>
                </li>
                <li><strong>رفض بعد التحكيم:</strong>
                    <ul>
                        <li>تعديلات طفيفة إلى متوسطة: 1-3 أشهر</li>
                        <li>تعديلات جوهرية: 3-6 أشهر</li>
                        <li>إعادة تصميم البحث: 6-12 شهراً</li>
                    </ul>
                </li>
                <li><strong>رفض مع إمكانية إعادة التقديم:</strong>
                    <ul>
                        <li>الالتزام بالمدة المحددة من المجلة (إن وجدت)</li>
                        <li>إذا لم تحدد المجلة مدة: 3-6 أشهر عموماً</li>
                    </ul>
                </li>
            </ul>
            <h4>نصائح مهمة:</h4>
            <ol>
                <li>خذ وقتاً كافياً لإجراء تعديلات جوهرية وليس مجرد تغييرات سطحية</li>
                <li>وازن بين السرعة وجودة التعديلات؛ فالجودة أهم من السرعة</li>
                <li>استخدم ملاحظات المحكمين كدليل لتحسين البحث، حتى عند التقديم لمجلة مختلفة</li>
                <li>احتفظ بسجل للتغييرات التي أجريتها استجابةً لتعليقات المحكمين</li>
                <li>قبل إعادة التقديم، اطلب من زملاء لم يشاركوا في البحث مراجعته</li>
                <li>في حالة التقديم لمجلة جديدة، تأكد من تعديل البحث ليتوافق مع متطلباتها وجمهورها</li>
            </ol>
            <div class="example-box">
                <h4>مثال لجدول زمني للتعديلات بعد الرفض:</h4>
                <table style="width:100%; border-collapse: collapse; text-align: right; direction: rtl;">
                    <tr style="background-color: #f2f2f2;">
                        <th style="border: 1px solid #ddd; padding: 8px;">المرحلة</th>
                        <th style="border: 1px solid #ddd; padding: 8px;">المدة التقديرية</th>
                        <th style="border: 1px solid #ddd; padding: 8px;">الأنشطة الرئيسية</th>
                    </tr>
                    <tr>
                        <td style="border: 1px solid #ddd; padding: 8px;">استيعاب وتحليل التعليقات</td>
                        <td style="border: 1px solid #ddd; padding: 8px;">1-2 أسبوع</td>
                        <td style="border: 1px solid #ddd; padding: 8px;">قراءة متأنية للتعليقات، تصنيفها، مناقشتها مع المشاركين في البحث، وضع خطة عمل</td>
                    </tr>
                    <tr>
                        <td style="border: 1px solid #ddd; padding: 8px;">تحديث مراجعة الأدبيات</td>
                        <td style="border: 1px solid #ddd; padding: 8px;">2-3 أسابيع</td>
                        <td style="border: 1px solid #ddd; padding: 8px;">البحث عن دراسات حديثة، قراءتها، دمجها في مراجعة الأدبيات، إعادة صياغة الفجوة البحثية</td>
                    </tr>
                    <tr>
                        <td style="border: 1px solid #ddd; padding: 8px;">تعديل المنهجية وإجراء تحليلات إضافية</td>
                        <td style="border: 1px solid #ddd; padding: 8px;">3-6 أسابيع</td>
                        <td style="border: 1px solid #ddd; padding: 8px;">توسيع العينة، تنقيح أدوات البحث، إجراء تحليلات إحصائية إضافية، تحليل الحساسية</td>
                    </tr>
                    <tr>
                        <td style="border: 1px solid #ddd; padding: 8px;">إعادة صياغة النتائج والمناقشة</td>
                        <td style="border: 1px solid #ddd; padding: 8px;">2-4 أسابيع</td>
                        <td style="border: 1px solid #ddd; padding: 8px;">دمج النتائج الجديدة، تعميق المناقشة، ربط النتائج بالأدبيات بشكل أفضل، تنقيح الاستنتاجات</td>
                    </tr>
                    <tr>
                        <td style="border: 1px solid #ddd; padding: 8px;">المراجعة اللغوية والتنسيق</td>
                        <td style="border: 1px solid #ddd; padding: 8px;">1-2 أسبوع</td>
                        <td style="border: 1px solid #ddd; padding: 8px;">تحسين اللغة والأسلوب، تنسيق البحث وفق متطلبات المجلة الجديدة، مراجعة المراجع والاقتباسات</td>
                    </tr>
                    <tr>
                        <td style="border: 1px solid #ddd; padding: 8px;">المراجعة النهائية وإعداد خطاب التقديم</td>
                        <td style="border: 1px solid #ddd; padding: 8px;">1 أسبوع</td>
                        <td style="border: 1px solid #ddd; padding: 8px;">مراجعة شاملة للبحث، كتابة خطاب تقديم قوي، تجهيز الملفات والمستندات المطلوبة للتقديم</td>
                    </tr>
                </table>
                <p>* المدد تقديرية وتختلف حسب حجم وطبيعة التعديلات المطلوبة.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

	with st.expander("هل أذكر في خطاب التقديم أن البحث تم رفضه من مجلة أخرى؟"):
		st.markdown("""
        <div class="step-box">
            <p>هذه مسألة تتطلب تفكيراً استراتيجياً، وليس هناك إجابة قاطعة تناسب جميع الحالات:</p>
            <h4>حالات يُنصح فيها بذكر الرفض السابق:</h4>
            <ul>
                <li>إذا كانت تعليقات المحكمين من المجلة السابقة مفيدة وقمت بإجراء تحسينات جوهرية بناءً عليها</li>
                <li>إذا كان الرفض من مجلة مرموقة جداً، وقد أشار المحكمون إلى أن البحث جيد ولكنه لا يتناسب مع مستوى المجلة العالي</li>
                <li>إذا أشار محرر المجلة السابقة صراحةً إلى أن البحث مناسب للمجلة التي تقدم إليها الآن</li>
                <li>إذا كان المجال صغيراً ومن المحتمل أن يكون بعض المحكمين مشتركين بين المجلتين</li>
            </ul>
            <h4>حالات يُفضل فيها عدم ذكر الرفض السابق:</h4>
            <ul>
                <li>إذا كان الرفض بسبب مشاكل جوهرية في المنهجية أو النتائج</li>
                <li>إذا كانت تعليقات المحكمين السابقين سلبية للغاية</li>
                <li>إذا كان البحث قد خضع لتغييرات جذرية بحيث أصبح بحثاً مختلفاً إلى حد كبير</li>
                <li>إذا لم يكن هناك سبب وجيه لذكر الرفض السابق</li>
            </ul>
            <h4>كيفية ذكر الرفض السابق (إذا قررت ذلك):</h4>
            <ol>
                <li>كن صريحاً ولكن إيجابياً، مع التركيز على التحسينات التي أجريتها</li>
                <li>لا تنتقد المجلة السابقة أو قرارها</li>
                <li>اشرح باختصار كيف استفدت من تعليقات المحكمين السابقين</li>
                <li>وضح كيف أصبح البحث الآن أكثر ملاءمة للمجلة الحالية</li>
            </ol>
            <div class="example-box">
                <h4>مثال لفقرة في خطاب التقديم تذكر الرفض السابق بطريقة إيجابية:</h4>
                <blockquote>
                    "أود أن أشير إلى أن نسخة سابقة من هذا البحث تم تقديمها إلى مجلة الاقتصاد العالمي في يناير 2025. على الرغم من أن البحث لم يتم قبوله للنشر، إلا أننا استفدنا كثيراً من تعليقات المحكمين الثلاثة. قمنا بإجراء تعديلات جوهرية على البحث استجابةً لهذه التعليقات، بما في ذلك توسيع العينة من 32 إلى 87 مشاركاً، وتحديث مراجعة الأدبيات لتشمل الدراسات الحديثة (2020-2025)، وإضافة تحليلات إحصائية متقدمة. نعتقد أن هذه التعديلات قد حسنت البحث بشكل كبير وجعلته أكثر ملاءمة لنطاق واهتمامات مجلتكم المرموقة."
                </blockquote>
            </div>
            <h4>نصائح إضافية:</h4>
            <ul>
                <li>لا تشعر بالإلزام بذكر جميع المجلات التي رفضت البحث سابقاً</li>
                <li>تأكد من أن النسخة المقدمة حالياً تختلف بشكل ملحوظ عن النسخة المرفوضة</li>
                <li>في حالة الشك، يمكن استشارة زملاء ذوي خبرة في النشر في المجلة المستهدفة</li>
                <li>بعض المجلات تطلب صراحةً في إرشادات التقديم ذكر التقديمات السابقة للبحث، وفي هذه الحالة يجب الالتزام بذلك</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

	with st.expander("ما هي أفضل استراتيجية لاختيار المجلة بعد الرفض؟"):
		st.markdown("""
        <div class="step-box">
            <p>اختيار المجلة المناسبة بعد الرفض يعتبر قراراً استراتيجياً مهماً:</p>
            <h4>استراتيجيات اختيار المجلة البديلة:</h4>
            <ol>
                <li><strong>التدرج في المستوى:</strong>
                    <ul>
                        <li>اختيار مجلة ذات معامل تأثير أقل قليلاً من المجلة السابقة</li>
                        <li>مناسبة عندما يكون سبب الرفض هو المستوى العالي للمجلة وليس جودة البحث</li>
                        <li>يمكن التدرج تدريجياً عبر مستويات المجلات حتى تجد المستوى المناسب</li>
                    </ul>
                </li>
                <li><strong>التخصص الأفضل:</strong>
                    <ul>
                        <li>اختيار مجلة أكثر تخصصاً وملاءمة لموضوع البحث</li>
                        <li>مناسبة عندما يكون سبب الرفض هو عدم ملاءمة الموضوع لنطاق المجلة</li>
                        <li>قد تكون المجلة المتخصصة أكثر تقديراً لقيمة البحث في مجالها المحدد</li>
                    </ul>
                </li>
                <li><strong>التوصية المباشرة:</strong>
                    <ul>
                        <li>اتباع توصية محرر المجلة السابقة بمجلات بديلة (إن وجدت)</li>
                        <li>ميزة هذه الاستراتيجية أن المحرر يعرف جيداً ما يناسب بحثك</li>
                        <li>قد يقدم المحرر أحياناً توصية للمحرر الجديد</li>
                    </ul>
                </li>
                <li><strong>النطاق الجغرافي:</strong>
                    <ul>
                        <li>اختيار مجلة ذات تركيز جغرافي أكثر ملاءمة للبحث</li>
                        <li>مناسبة للبحوث ذات السياق المحلي أو الإقليمي</li>
                        <li>مثال: التحول من مجلة عالمية إلى مجلة إقليمية أو محلية</li>
                    </ul>
                </li>
                <li><strong>المنهجية المتوافقة:</strong>
                    <ul>
                        <li>اختيار مجلة تفضل المنهجية المستخدمة في البحث</li>
                        <li>مناسبة عندما يكون سبب الرفض هو عدم تفضيل المجلة للمنهجية المستخدمة</li>
                        <li>مثال: مجلات تفضل البحوث النوعية vs الكمية، أو النظرية vs التطبيقية</li>
                    </ul>
                </li>
            </ol>
            <h4>عوامل يجب مراعاتها عند اختيار المجلة البديلة:</h4>
            <ul>
                <li><strong>نطاق المجلة واهتماماتها:</strong> تأكد من قراءة "نطاق وأهداف" المجلة بعناية</li>
                <li><strong>الجمهور المستهدف:</strong> هل جمهور المجلة سيهتم ببحثك؟</li>
                <li><strong>أسلوب وتنسيق المجلة:</strong> اطلع على أبحاث منشورة فيها لفهم الأسلوب المفضل</li>
                <li><strong>معدل القبول:</strong> ابحث عن إحصائيات حول معدلات القبول في المجلة</li>
                <li><strong>سرعة النشر:</strong> ما هي المدة المتوقعة من التقديم إلى النشر؟</li>
                <li><strong>سمعة المجلة في تخصصك:</strong> استشر زملاء متخصصين حول سمعة المجلة</li>
                <li><strong>سياسة المجلة تجاه التقديمات السابقة:</strong> هل تقبل المجلة أبحاثاً سبق رفضها من مجلات أخرى؟</li>
            </ul>
            <h4>أدوات مساعدة في اختيار المجلة:</h4>
            <ul>
                <li>Journal Finder من Elsevier</li>
                <li>Journal Suggester من Springer</li>
                <li>Journal Selector من MDPI</li>
                <li>Find the right journal من Wiley</li>
                <li>Jane (Journal/Author Name Estimator)</li>
                <li>قواعد بيانات تصنيف المجلات مثل Scimago وWeb of Science</li>
            </ul>
            <div class="example-box">
                <h4>مثال لاستراتيجية اختيار المجلة بعد الرفض:</h4>
                <p>بحث عن "أثر التمويل الإسلامي على التنمية الاقتصادية في دول الخليج" تم رفضه من مجلة Journal of International Economics (JIE) - مجلة عالمية مرموقة في الاقتصاد الدولي.</p>
                <p><strong>سبب الرفض:</strong> "البحث يركز بشكل كبير على منطقة جغرافية محددة وعلى قطاع مالي متخصص، مما يجعله أقل ملاءمة لجمهور المجلة العالمي."</p>
                <p><strong>خيارات المجلات البديلة وفق استراتيجيات مختلفة:</strong></p>
                <ol>
                    <li><strong>التخصص الأفضل:</strong> Journal of Islamic Accounting and Business Research</li>
                    <li><strong>النطاق الجغرافي:</strong> Middle Eastern Finance and Economics</li>
                    <li><strong>التدرج في المستوى:</strong> Economic Development and Cultural Change (معامل تأثير أقل من JIE)</li>
                    <li><strong>المنهجية المتوافقة:</strong> International Journal of Islamic and Middle Eastern Finance and Management (تقبل الدراسات التطبيقية للتمويل الإسلامي)</li>
                </ol>
                <p><strong>الاختيار النهائي:</strong> Journal of Islamic Accounting and Business Research - مجلة متخصصة في التمويل الإسلامي ذات سمعة جيدة في هذا المجال المتخصص.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

	with st.expander("أين يمكنني إيجاد مصادر إضافية حول الكتابة والنشر الأكاديمي؟"):
		st.markdown("""
        <div class="step-box">
            <p>هناك العديد من المصادر الممتازة المتاحة عبر الإنترنت وفي الكتب. إليك بعض الاقتراحات:</p>
            <ul>
                <li><strong>مواقع الجامعات ومراكز الكتابة:</strong> العديد من الجامعات المرموقة تقدم أدلة وموارد مجانية حول الكتابة الأكاديمية والنشر (مثلاً، Purdue OWL, Harvard Writing Center).</li>
                <li><strong>مواقع الناشرين الكبار:</strong> Elsevier, Springer, Wiley, Taylor & Francis لديهم أقسام للمؤلفين تقدم نصائح وموارد قيمة.</li>
                <li><strong>كتب متخصصة:</strong> مثل:
                    <ul>
                        <li>"The Elements of Style" by Strunk and White (لأساسيات الكتابة الواضحة بالإنجليزية).</li>
                        <li>"Writing Your Journal Article in Twelve Weeks" by Wendy Laura Belcher.</li>
                        <li>"How to Write a Lot: A Practical Guide to Productive Academic Writing" by Paul J. Silvia.</li>
                    </ul>
                </li>
                <li><strong>ورش عمل ودورات تدريبية:</strong> تقدمها العديد من المؤسسات الأكاديمية أو المنصات التعليمية عبر الإنترنت.</li>
                <li><strong>مدونات ومنتديات للباحثين:</strong> مثل "The Thesis Whisperer" أو مجموعات النقاش المتخصصة.</li>
                <li><strong>أدوات مساعدة للكتابة والتحرير:</strong> مثل Grammarly, Zotero/Mendeley (لإدارة المراجع), LaTeX (للتنسيق المتقدم).</li>
            </ul>
            <p>من المهم أيضاً قراءة الأبحاث المنشورة في مجالك بانتظام، والانتباه إلى أسلوب الكتابة وهيكلة المقالات الناجحة.</p>
        </div>
        """, unsafe_allow_html=True)

	st.markdown("""
    <div class="success-box">
        <h3>ملخص النصائح النهائية</h3>
        <ul>
            <li>اعتبر رفض البحث جزءاً طبيعياً ومفيداً من المسيرة الأكاديمية وليس انعكاساً لقيمتك كباحث.</li>
            <li>استفد من كل تعليق وكل تجربة رفض لتحسين بحثك الحالي وأبحاثك المستقبلية.</li>
            <li>طور استراتيجية واضحة للتعامل مع الرفض، بدءاً من تحليل الأسباب وحتى اختيار المجلة البديلة.</li>
            <li>اعمل على تحسين مهاراتك البحثية والكتابية والتحليلية باستمرار.</li>
            <li>تواصل مع باحثين آخرين، كون شبكة دعم، واطلب النصيحة والمساعدة عند الحاجة.</li>
            <li>احتفظ بسجل لتجاربك مع المجلات المختلفة (أسباب الرفض، سرعة الرد، جودة التحكيم) للاستفادة منها في المستقبل.</li>
            <li>تذكر أن العديد من الأبحاث المؤثرة والمهمة مرت بمرحلة رفض أو أكثر قبل نشرها. المثابرة هي مفتاح النجاح.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)


# تعريف الصفحات في التطبيق
def main():
	st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2921/2921930.png", width=80, use_column_width='auto')
	st.sidebar.title("دليل التعامل مع رفض المقالات")  # Raw

	pages_dict = {
		"الصفحة الرئيسية": main_page,
		"أسباب رفض المقالات": rejection_reasons_page,
		"أنواع قرارات الرفض": rejection_types_page,
		"تحليل تعليقات المحكمين": reviewers_comments_page,
		"استراتيجيات الرد والتعديل": response_strategies_page,
		"الأسئلة الشائعة": faq_page
	}

	# Use raw Arabic page names for display in sidebar radio
	# Streamlit should handle RTL for radio button labels with CSS

	st.sidebar.markdown("---")
	selected_page_key = st.sidebar.radio("اختر الصفحة:", list(pages_dict.keys()),
										 format_func=lambda x: x)  # Raw label, raw options

	# عرض الصفحة المختارة
	pages_dict[selected_page_key]()

	st.sidebar.markdown("---")
	st.sidebar.markdown(f"""
    <div style="text-align: center; direction: rtl; padding: 10px;">
        <p>تم إعداد هذا الدليل لمساعدة الباحثين في مجال الاقتصاد على التعامل بفعالية مع تحديات النشر العلمي.</p>
        <p>© 2025 - إصدار تجريبي</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
	main()
