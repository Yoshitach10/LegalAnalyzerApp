{\rtf1\ansi\ansicpg1252\cocoartf2822
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fnil\fcharset0 Menlo-Regular;}
{\colortbl;\red255\green255\blue255;\red183\green111\blue179;\red0\green0\blue0;\red255\green255\blue255;
\red106\green152\blue85;\red194\green126\blue101;\red202\green202\blue202;\red140\green211\blue254;\red70\green137\blue204;
\red212\green214\blue154;\red196\green83\blue86;\red167\green197\blue152;\red67\green192\blue160;}
{\*\expandedcolortbl;;\cssrgb\c77255\c52549\c75294;\cssrgb\c0\c0\c0;\cssrgb\c100000\c100000\c100000;
\cssrgb\c48627\c65098\c40784;\cssrgb\c80784\c56863\c47059;\cssrgb\c83137\c83137\c83137;\cssrgb\c61176\c86275\c99608;\cssrgb\c33725\c61176\c83922;
\cssrgb\c86275\c86275\c66667;\cssrgb\c81961\c41176\c41176;\cssrgb\c70980\c80784\c65882;\cssrgb\c30588\c78824\c69020;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\deftab720
\pard\pardeftab720\partightenfactor0

\f0\fs24 \cf2 \cb3 \expnd0\expndtw0\kerning0
\outl0\strokewidth0 \strokec2 import\cf4 \strokec4  streamlit \cf2 \strokec2 as\cf4 \strokec4  st\cb1 \
\cf2 \cb3 \strokec2 import\cf4 \strokec4  fitz  \cf5 \strokec5 # PyMuPDF\cf4 \cb1 \strokec4 \
\cf2 \cb3 \strokec2 import\cf4 \strokec4  re\cb1 \
\cf2 \cb3 \strokec2 from\cf4 \strokec4  sklearn.feature_extraction.text \cf2 \strokec2 import\cf4 \strokec4  TfidfVectorizer\cb1 \
\cf2 \cb3 \strokec2 from\cf4 \strokec4  sklearn.metrics.pairwise \cf2 \strokec2 import\cf4 \strokec4  cosine_similarity\cb1 \
\cf2 \cb3 \strokec2 from\cf4 \strokec4  transformers \cf2 \strokec2 import\cf4 \strokec4  pipeline\cb1 \
\cf2 \cb3 \strokec2 from\cf4 \strokec4  openai \cf2 \strokec2 import\cf4 \strokec4  OpenAI\cb1 \
\cf2 \cb3 \strokec2 import\cf4 \strokec4  openai\cb1 \
\cf2 \cb3 \strokec2 import\cf4 \strokec4  numpy \cf2 \strokec2 as\cf4 \strokec4  np\cb1 \
\
\pard\pardeftab720\partightenfactor0
\cf5 \cb3 \strokec5 # --- App UI ---\cf4 \cb1 \strokec4 \
\pard\pardeftab720\partightenfactor0
\cf4 \cb3 st.title(\cf6 \strokec6 "AI-Powered Legal Document Analyzer"\cf4 \strokec4 )\cb1 \
\cb3 st.write(\cf6 \strokec6 "Upload a legal document (PDF) to extract its raw text, summarize it, extract clauses, and compare them."\cf4 \strokec4 )\cb1 \
\
\pard\pardeftab720\partightenfactor0
\cf5 \cb3 \strokec5 # --- Upload PDF ---\cf4 \cb1 \strokec4 \
\pard\pardeftab720\partightenfactor0
\cf4 \cb3 uploaded_file \cf7 \strokec7 =\cf4 \strokec4  st.file_uploader(\cf6 \strokec6 "Choose a legal PDF file"\cf4 \strokec4 , \cf8 \strokec8 type\cf7 \strokec7 =\cf6 \strokec6 "pdf"\cf4 \strokec4 )\cb1 \
\
\pard\pardeftab720\partightenfactor0
\cf5 \cb3 \strokec5 # --- PDF text extraction ---\cf4 \cb1 \strokec4 \
\pard\pardeftab720\partightenfactor0
\cf9 \cb3 \strokec9 def\cf4 \strokec4  \cf10 \strokec10 extract_text\cf4 \strokec4 (\cf8 \strokec8 uploaded_file\cf4 \strokec4 ):\cb1 \
\pard\pardeftab720\partightenfactor0
\cf4 \cb3     doc \cf7 \strokec7 =\cf4 \strokec4  fitz.open(\cf8 \strokec8 stream\cf7 \strokec7 =\cf4 \strokec4 uploaded_file.read(), \cf8 \strokec8 filetype\cf7 \strokec7 =\cf6 \strokec6 "pdf"\cf4 \strokec4 )\cb1 \
\cb3     text \cf7 \strokec7 =\cf4 \strokec4  \cf6 \strokec6 ""\cf4 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 for\cf4 \strokec4  page \cf2 \strokec2 in\cf4 \strokec4  doc:\cb1 \
\cb3         text \cf7 \strokec7 +=\cf4 \strokec4  page.get_text()\cb1 \
\cb3     \cf2 \strokec2 return\cf4 \strokec4  text\cb1 \
\
\pard\pardeftab720\partightenfactor0
\cf5 \cb3 \strokec5 # --- Summarization Model ---\cf4 \cb1 \strokec4 \
\pard\pardeftab720\partightenfactor0
\cf10 \cb3 \strokec10 @st.cache_resource\cf4 \cb1 \strokec4 \
\pard\pardeftab720\partightenfactor0
\cf9 \cb3 \strokec9 def\cf4 \strokec4  \cf10 \strokec10 load_summarizer\cf4 \strokec4 ():\cb1 \
\pard\pardeftab720\partightenfactor0
\cf4 \cb3     \cf2 \strokec2 return\cf4 \strokec4  pipeline(\cf6 \strokec6 "summarization"\cf4 \strokec4 , \cf8 \strokec8 model\cf7 \strokec7 =\cf6 \strokec6 "sshleifer/distilbart-cnn-12-6"\cf4 \strokec4 )\cb1 \
\
\cb3 summarizer \cf7 \strokec7 =\cf4 \strokec4  load_summarizer()\cb1 \
\
\pard\pardeftab720\partightenfactor0
\cf5 \cb3 \strokec5 # --- Clause Keywords & Standard Clauses ---\cf4 \cb1 \strokec4 \
\pard\pardeftab720\partightenfactor0
\cf4 \cb3 clause_keywords \cf7 \strokec7 =\cf4 \strokec4  \{\cb1 \
\cb3     \cf6 \strokec6 "Confidentiality"\cf4 \strokec4 : [\cf6 \strokec6 "confidential"\cf4 \strokec4 , \cf6 \strokec6 "non-disclosure"\cf4 \strokec4 , \cf6 \strokec6 "privacy"\cf4 \strokec4 ],\cb1 \
\cb3     \cf6 \strokec6 "Termination"\cf4 \strokec4 : [\cf6 \strokec6 "terminate"\cf4 \strokec4 , \cf6 \strokec6 "termination"\cf4 \strokec4 , \cf6 \strokec6 "cancel"\cf4 \strokec4 , \cf6 \strokec6 "end of agreement"\cf4 \strokec4 ],\cb1 \
\cb3     \cf6 \strokec6 "Payment"\cf4 \strokec4 : [\cf6 \strokec6 "payment"\cf4 \strokec4 , \cf6 \strokec6 "compensation"\cf4 \strokec4 , \cf6 \strokec6 "fee"\cf4 \strokec4 , \cf6 \strokec6 "remuneration"\cf4 \strokec4 ],\cb1 \
\cb3     \cf6 \strokec6 "Governing Law"\cf4 \strokec4 : [\cf6 \strokec6 "jurisdiction"\cf4 \strokec4 , \cf6 \strokec6 "governing law"\cf4 \strokec4 , \cf6 \strokec6 "under the laws of"\cf4 \strokec4 ],\cb1 \
\cb3     \cf6 \strokec6 "Indemnity"\cf4 \strokec4 : [\cf6 \strokec6 "indemnify"\cf4 \strokec4 , \cf6 \strokec6 "liability"\cf4 \strokec4 , \cf6 \strokec6 "hold harmless"\cf4 \strokec4 ],\cb1 \
\cb3     \cf6 \strokec6 "Force Majeure"\cf4 \strokec4 : [\cf6 \strokec6 "force majeure"\cf4 \strokec4 , \cf6 \strokec6 "act of god"\cf4 \strokec4 , \cf6 \strokec6 "unforeseen circumstances"\cf4 \strokec4 ],\cb1 \
\cb3     \cf6 \strokec6 "Dispute Resolution"\cf4 \strokec4 : [\cf6 \strokec6 "arbitration"\cf4 \strokec4 , \cf6 \strokec6 "dispute"\cf4 \strokec4 , \cf6 \strokec6 "litigation"\cf4 \strokec4 , \cf6 \strokec6 "settlement"\cf4 \strokec4 ]\cb1 \
\cb3 \}\cb1 \
\
\cb3 standard_clauses \cf7 \strokec7 =\cf4 \strokec4  \{\cb1 \
\cb3     \cf6 \strokec6 "termination"\cf4 \strokec4 : \cf6 \strokec6 "This agreement may be terminated by either party upon giving written notice of 30 days."\cf4 \strokec4 ,\cb1 \
\cb3     \cf6 \strokec6 "liability"\cf4 \strokec4 : \cf6 \strokec6 "The liability of the parties shall be limited to direct damages only."\cf4 \strokec4 ,\cb1 \
\cb3     \cf6 \strokec6 "dispute_resolution"\cf4 \strokec4 : \cf6 \strokec6 "Any disputes arising shall be resolved through arbitration in accordance with applicable laws."\cf4 \strokec4 ,\cb1 \
\cb3     \cf6 \strokec6 "confidentiality"\cf4 \strokec4 : \cf6 \strokec6 "Parties agree to maintain the confidentiality of shared information during and after the agreement term."\cf4 \cb1 \strokec4 \
\cb3 \}\cb1 \
\
\pard\pardeftab720\partightenfactor0
\cf5 \cb3 \strokec5 # --- Clause Extraction ---\cf4 \cb1 \strokec4 \
\pard\pardeftab720\partightenfactor0
\cf9 \cb3 \strokec9 def\cf4 \strokec4  \cf10 \strokec10 extract_clauses\cf4 \strokec4 (\cf8 \strokec8 text\cf4 \strokec4 ):\cb1 \
\pard\pardeftab720\partightenfactor0
\cf4 \cb3     extracted_clauses \cf7 \strokec7 =\cf4 \strokec4  \{\}\cb1 \
\cb3     sentences \cf7 \strokec7 =\cf4 \strokec4  re.split(\cf9 \strokec9 r\cf11 \strokec11 '\cf7 \strokec7 (?<=\cf11 \strokec11 [\cf9 \strokec9 .!?\cf11 \strokec11 ]\cf7 \strokec7 )\cf11 \strokec11  \cf7 \strokec7 +\cf11 \strokec11 '\cf4 \strokec4 , text)\cb1 \
\cb3     \cf2 \strokec2 for\cf4 \strokec4  clause, keywords \cf2 \strokec2 in\cf4 \strokec4  clause_keywords.items():\cb1 \
\cb3         matched_sentences \cf7 \strokec7 =\cf4 \strokec4  [s.strip() \cf2 \strokec2 for\cf4 \strokec4  s \cf2 \strokec2 in\cf4 \strokec4  sentences \cf2 \strokec2 if\cf4 \strokec4  \cf10 \strokec10 any\cf4 \strokec4 (k.lower() \cf2 \strokec2 in\cf4 \strokec4  s.lower() \cf2 \strokec2 for\cf4 \strokec4  k \cf2 \strokec2 in\cf4 \strokec4  keywords)]\cb1 \
\cb3         \cf2 \strokec2 if\cf4 \strokec4  matched_sentences:\cb1 \
\cb3             extracted_clauses[clause] \cf7 \strokec7 =\cf4 \strokec4  matched_sentences\cb1 \
\cb3     \cf2 \strokec2 return\cf4 \strokec4  extracted_clauses\cb1 \
\
\pard\pardeftab720\partightenfactor0
\cf5 \cb3 \strokec5 # --- Compare Clauses ---\cf4 \cb1 \strokec4 \
\pard\pardeftab720\partightenfactor0
\cf9 \cb3 \strokec9 def\cf4 \strokec4  \cf10 \strokec10 compare_with_standard_clauses\cf4 \strokec4 (\cf8 \strokec8 clauses\cf4 \strokec4 , \cf8 \strokec8 standard_clauses\cf4 \strokec4 ):\cb1 \
\pard\pardeftab720\partightenfactor0
\cf4 \cb3     comparisons \cf7 \strokec7 =\cf4 \strokec4  []\cb1 \
\cb3     \cf2 \strokec2 for\cf4 \strokec4  clause \cf2 \strokec2 in\cf4 \strokec4  clauses:\cb1 \
\cb3         max_similarity \cf7 \strokec7 =\cf4 \strokec4  \cf12 \strokec12 0\cf4 \cb1 \strokec4 \
\cb3         best_match \cf7 \strokec7 =\cf4 \strokec4  \cf6 \strokec6 ""\cf4 \cb1 \strokec4 \
\cb3         \cf2 \strokec2 for\cf4 \strokec4  label, standard \cf2 \strokec2 in\cf4 \strokec4  standard_clauses.items():\cb1 \
\cb3             vectorizer \cf7 \strokec7 =\cf4 \strokec4  TfidfVectorizer().fit_transform([clause, standard])\cb1 \
\cb3             similarity \cf7 \strokec7 =\cf4 \strokec4  cosine_similarity(vectorizer[\cf12 \strokec12 0\cf4 \strokec4 :\cf12 \strokec12 1\cf4 \strokec4 ], vectorizer[\cf12 \strokec12 1\cf4 \strokec4 :\cf12 \strokec12 2\cf4 \strokec4 ])[\cf12 \strokec12 0\cf4 \strokec4 ][\cf12 \strokec12 0\cf4 \strokec4 ]\cb1 \
\cb3             \cf2 \strokec2 if\cf4 \strokec4  similarity \cf7 \strokec7 >\cf4 \strokec4  max_similarity:\cb1 \
\cb3                 max_similarity \cf7 \strokec7 =\cf4 \strokec4  similarity\cb1 \
\cb3                 best_match \cf7 \strokec7 =\cf4 \strokec4  standard\cb1 \
\cb3         comparisons.append((clause, best_match, \cf10 \strokec10 round\cf4 \strokec4 (max_similarity, \cf12 \strokec12 2\cf4 \strokec4 )))\cb1 \
\cb3     \cf2 \strokec2 return\cf4 \strokec4  comparisons\cb1 \
\
\pard\pardeftab720\partightenfactor0
\cf5 \cb3 \strokec5 # --- Risk Detection ---\cf4 \cb1 \strokec4 \
\pard\pardeftab720\partightenfactor0
\cf9 \cb3 \strokec9 def\cf4 \strokec4  \cf10 \strokec10 find_risky_clauses\cf4 \strokec4 (\cf8 \strokec8 clauses\cf4 \strokec4 , \cf8 \strokec8 risky_keywords\cf4 \strokec4 ):\cb1 \
\pard\pardeftab720\partightenfactor0
\cf4 \cb3     risky \cf7 \strokec7 =\cf4 \strokec4  []\cb1 \
\cb3     \cf2 \strokec2 for\cf4 \strokec4  clause \cf2 \strokec2 in\cf4 \strokec4  clauses:\cb1 \
\cb3         \cf2 \strokec2 for\cf4 \strokec4  keyword \cf2 \strokec2 in\cf4 \strokec4  risky_keywords:\cb1 \
\cb3             \cf2 \strokec2 if\cf4 \strokec4  keyword.lower() \cf9 \strokec9 in\cf4 \strokec4  clause.lower():\cb1 \
\cb3                 risky.append(clause)\cb1 \
\cb3                 \cf2 \strokec2 break\cf4 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 return\cf4 \strokec4  risky\cb1 \
\
\pard\pardeftab720\partightenfactor0
\cf5 \cb3 \strokec5 # --- Suggest Clause Rewrite with OpenAI (Latest API) ---\cf4 \cb1 \strokec4 \
\pard\pardeftab720\partightenfactor0
\cf9 \cb3 \strokec9 def\cf4 \strokec4  \cf10 \strokec10 suggest_better_clause\cf4 \strokec4 (\cf8 \strokec8 clause\cf4 \strokec4 ):\cb1 \
\pard\pardeftab720\partightenfactor0
\cf4 \cb3     prompt \cf7 \strokec7 =\cf4 \strokec4  (\cb1 \
\cb3         \cf6 \strokec6 "You are a legal expert. Rewrite the following clause to make it safer, clearer, and more legally sound:\cf9 \strokec9 \\n\\n\cf6 \strokec6 "\cf4 \cb1 \strokec4 \
\cb3         \cf9 \strokec9 f\cf6 \strokec6 "Original Clause:\cf9 \strokec9 \\n\{\cf4 \strokec4 clause\cf9 \strokec9 \}\\n\\n\cf6 \strokec6 "\cf4 \cb1 \strokec4 \
\cb3         \cf6 \strokec6 "Improved Clause:"\cf4 \cb1 \strokec4 \
\cb3     )\cb1 \
\cb3     \cf2 \strokec2 try\cf4 \strokec4 :\cb1 \
\cb3         client \cf7 \strokec7 =\cf4 \strokec4  OpenAI()\cb1 \
\cb3         response \cf7 \strokec7 =\cf4 \strokec4  client.chat.completions.create(\cb1 \
\cb3             \cf8 \strokec8 model\cf7 \strokec7 =\cf6 \strokec6 "gpt-3.5-turbo"\cf4 \strokec4 ,\cb1 \
\cb3             \cf8 \strokec8 messages\cf7 \strokec7 =\cf4 \strokec4 [\cb1 \
\cb3                 \{\cf6 \strokec6 "role"\cf4 \strokec4 : \cf6 \strokec6 "user"\cf4 \strokec4 , \cf6 \strokec6 "content"\cf4 \strokec4 : prompt\}\cb1 \
\cb3             ],\cb1 \
\cb3             \cf8 \strokec8 temperature\cf7 \strokec7 =\cf12 \strokec12 0.4\cf4 \cb1 \strokec4 \
\cb3         )\cb1 \
\cb3         improved \cf7 \strokec7 =\cf4 \strokec4  response.choices[\cf12 \strokec12 0\cf4 \strokec4 ].message.content.strip()\cb1 \
\cb3         \cf2 \strokec2 return\cf4 \strokec4  improved\cb1 \
\cb3     \cf2 \strokec2 except\cf4 \strokec4  \cf13 \strokec13 Exception\cf4 \strokec4  \cf2 \strokec2 as\cf4 \strokec4  e:\cb1 \
\cb3         \cf2 \strokec2 return\cf4 \strokec4  \cf9 \strokec9 f\cf6 \strokec6 "Error: \cf9 \strokec9 \{\cf13 \strokec13 str\cf4 \strokec4 (e)\cf9 \strokec9 \}\cf6 \strokec6 "\cf4 \cb1 \strokec4 \
\
\pard\pardeftab720\partightenfactor0
\cf5 \cb3 \strokec5 # --- Main Workflow ---\cf4 \cb1 \strokec4 \
\pard\pardeftab720\partightenfactor0
\cf2 \cb3 \strokec2 if\cf4 \strokec4  uploaded_file \cf9 \strokec9 is\cf4 \strokec4  \cf9 \strokec9 not\cf4 \strokec4  \cf9 \strokec9 None\cf4 \strokec4 :\cb1 \
\pard\pardeftab720\partightenfactor0
\cf4 \cb3     text \cf7 \strokec7 =\cf4 \strokec4  extract_text(uploaded_file)\cb1 \
\
\cb3     \cf2 \strokec2 if\cf4 \strokec4  text.strip():\cb1 \
\cb3         st.subheader(\cf6 \strokec6 "Extracted Text"\cf4 \strokec4 )\cb1 \
\cb3         st.text_area(\cf6 \strokec6 "Raw Text from PDF"\cf4 \strokec4 , text, \cf8 \strokec8 height\cf7 \strokec7 =\cf12 \strokec12 400\cf4 \strokec4 )\cb1 \
\
\cb3         \cf2 \strokec2 if\cf4 \strokec4  st.button(\cf6 \strokec6 "Summarize Text"\cf4 \strokec4 ):\cb1 \
\cb3             \cf2 \strokec2 with\cf4 \strokec4  st.spinner(\cf6 \strokec6 "Summarizing..."\cf4 \strokec4 ):\cb1 \
\cb3                 summary \cf7 \strokec7 =\cf4 \strokec4  summarizer(text[:\cf12 \strokec12 1024\cf4 \strokec4 ], \cf8 \strokec8 max_length\cf7 \strokec7 =\cf12 \strokec12 130\cf4 \strokec4 , \cf8 \strokec8 min_length\cf7 \strokec7 =\cf12 \strokec12 30\cf4 \strokec4 , \cf8 \strokec8 do_sample\cf7 \strokec7 =\cf9 \strokec9 False\cf4 \strokec4 )[\cf12 \strokec12 0\cf4 \strokec4 ][\cf6 \strokec6 'summary_text'\cf4 \strokec4 ]\cb1 \
\cb3                 st.subheader(\cf6 \strokec6 "Summary:"\cf4 \strokec4 )\cb1 \
\cb3                 st.write(summary)\cb1 \
\
\cb3         \cf2 \strokec2 if\cf4 \strokec4  st.button(\cf6 \strokec6 "Extract Clauses"\cf4 \strokec4 ):\cb1 \
\cb3             \cf2 \strokec2 with\cf4 \strokec4  st.spinner(\cf6 \strokec6 "Extracting Clauses..."\cf4 \strokec4 ):\cb1 \
\cb3                 clauses_dict \cf7 \strokec7 =\cf4 \strokec4  extract_clauses(text)\cb1 \
\cb3                 \cf2 \strokec2 if\cf4 \strokec4  clauses_dict:\cb1 \
\cb3                     \cf2 \strokec2 for\cf4 \strokec4  title, lines \cf2 \strokec2 in\cf4 \strokec4  clauses_dict.items():\cb1 \
\cb3                         st.subheader(\cf9 \strokec9 f\cf6 \strokec6 "\cf9 \strokec9 \{\cf4 \strokec4 title\cf9 \strokec9 \}\cf6 \strokec6  Clause"\cf4 \strokec4 )\cb1 \
\cb3                         \cf2 \strokec2 for\cf4 \strokec4  l \cf2 \strokec2 in\cf4 \strokec4  lines:\cb1 \
\cb3                             st.write(\cf9 \strokec9 f\cf6 \strokec6 "- \cf9 \strokec9 \{\cf4 \strokec4 l\cf9 \strokec9 \}\cf6 \strokec6 "\cf4 \strokec4 )\cb1 \
\
\cb3                     flattened \cf7 \strokec7 =\cf4 \strokec4  [clause \cf2 \strokec2 for\cf4 \strokec4  sublist \cf2 \strokec2 in\cf4 \strokec4  clauses_dict.values() \cf2 \strokec2 for\cf4 \strokec4  clause \cf2 \strokec2 in\cf4 \strokec4  sublist]\cb1 \
\cb3                     risky_keywords \cf7 \strokec7 =\cf4 \strokec4  [\cf6 \strokec6 "risky"\cf4 \strokec4 , \cf6 \strokec6 "dangerous"\cf4 \strokec4 ]\cb1 \
\cb3                     risky \cf7 \strokec7 =\cf4 \strokec4  find_risky_clauses(flattened, risky_keywords)\cb1 \
\
\cb3                     st.subheader(\cf6 \strokec6 "Risky Clauses Found:"\cf4 \strokec4 )\cb1 \
\cb3                     \cf2 \strokec2 if\cf4 \strokec4  risky:\cb1 \
\cb3                         \cf2 \strokec2 for\cf4 \strokec4  item \cf2 \strokec2 in\cf4 \strokec4  risky:\cb1 \
\cb3                             st.write(\cf9 \strokec9 f\cf6 \strokec6 "- \cf9 \strokec9 \{\cf4 \strokec4 item\cf9 \strokec9 \}\cf6 \strokec6 "\cf4 \strokec4 )\cb1 \
\cb3                     \cf2 \strokec2 else\cf4 \strokec4 :\cb1 \
\cb3                         st.success(\cf6 \strokec6 "No risky clauses detected."\cf4 \strokec4 )\cb1 \
\cb3                 \cf2 \strokec2 else\cf4 \strokec4 :\cb1 \
\cb3                     st.warning(\cf6 \strokec6 "No clauses detected."\cf4 \strokec4 )\cb1 \
\
\cb3         \cf2 \strokec2 if\cf4 \strokec4  st.button(\cf6 \strokec6 "Compare Clauses"\cf4 \strokec4 ):\cb1 \
\cb3             clauses_dict \cf7 \strokec7 =\cf4 \strokec4  extract_clauses(text)\cb1 \
\cb3             all_clauses \cf7 \strokec7 =\cf4 \strokec4  [c \cf2 \strokec2 for\cf4 \strokec4  sublist \cf2 \strokec2 in\cf4 \strokec4  clauses_dict.values() \cf2 \strokec2 for\cf4 \strokec4  c \cf2 \strokec2 in\cf4 \strokec4  sublist]\cb1 \
\cb3             comparisons \cf7 \strokec7 =\cf4 \strokec4  compare_with_standard_clauses(all_clauses, standard_clauses)\cb1 \
\
\cb3             st.subheader(\cf6 \strokec6 "Clause Comparison Results"\cf4 \strokec4 )\cb1 \
\cb3             \cf2 \strokec2 for\cf4 \strokec4  i, (clause, standard, similarity) \cf2 \strokec2 in\cf4 \strokec4  \cf10 \strokec10 enumerate\cf4 \strokec4 (comparisons):\cb1 \
\cb3                 st.markdown(\cf9 \strokec9 f\cf6 \strokec6 "**Extracted Clause \cf9 \strokec9 \{\cf4 \strokec4 i\cf7 \strokec7 +\cf12 \strokec12 1\cf9 \strokec9 \}\cf6 \strokec6 :** \cf9 \strokec9 \{\cf4 \strokec4 clause\cf9 \strokec9 \}\cf6 \strokec6 "\cf4 \strokec4 )\cb1 \
\cb3                 st.markdown(\cf9 \strokec9 f\cf6 \strokec6 "**Standard Clause:** \cf9 \strokec9 \{\cf4 \strokec4 standard\cf9 \strokec9 \}\cf6 \strokec6 "\cf4 \strokec4 )\cb1 \
\cb3                 st.markdown(\cf9 \strokec9 f\cf6 \strokec6 "**Similarity Score:** \cf9 \strokec9 \{\cf4 \strokec4 similarity\cf9 \strokec9 \}\cf6 \strokec6 "\cf4 \strokec4 )\cb1 \
\cb3                 st.markdown(\cf6 \strokec6 "---"\cf4 \strokec4 )\cb1 \
\
\cb3         \cf2 \strokec2 if\cf4 \strokec4  st.button(\cf6 \strokec6 "Suggest Better Wording"\cf4 \strokec4 ):\cb1 \
\cb3             clauses_dict \cf7 \strokec7 =\cf4 \strokec4  extract_clauses(text)\cb1 \
\cb3             all_clauses \cf7 \strokec7 =\cf4 \strokec4  [c \cf2 \strokec2 for\cf4 \strokec4  sublist \cf2 \strokec2 in\cf4 \strokec4  clauses_dict.values() \cf2 \strokec2 for\cf4 \strokec4  c \cf2 \strokec2 in\cf4 \strokec4  sublist]\cb1 \
\cb3             st.subheader(\cf6 \strokec6 "Improved Clause Suggestions"\cf4 \strokec4 )\cb1 \
\cb3             \cf2 \strokec2 for\cf4 \strokec4  i, clause \cf2 \strokec2 in\cf4 \strokec4  \cf10 \strokec10 enumerate\cf4 \strokec4 (all_clauses):\cb1 \
\cb3                 improved \cf7 \strokec7 =\cf4 \strokec4  suggest_better_clause(clause)\cb1 \
\cb3                 st.markdown(\cf9 \strokec9 f\cf6 \strokec6 "**Original Clause \cf9 \strokec9 \{\cf4 \strokec4 i\cf7 \strokec7 +\cf12 \strokec12 1\cf9 \strokec9 \}\cf6 \strokec6 :** \cf9 \strokec9 \{\cf4 \strokec4 clause\cf9 \strokec9 \}\cf6 \strokec6 "\cf4 \strokec4 )\cb1 \
\cb3                 st.markdown(\cf9 \strokec9 f\cf6 \strokec6 "**Suggested Rewrite:** \cf9 \strokec9 \{\cf4 \strokec4 improved\cf9 \strokec9 \}\cf6 \strokec6 "\cf4 \strokec4 )\cb1 \
\cb3                 st.markdown(\cf6 \strokec6 "---"\cf4 \strokec4 )\cb1 \
\
\cb3     \cf2 \strokec2 else\cf4 \strokec4 :\cb1 \
\cb3         st.warning(\cf6 \strokec6 "Could not extract any text. Please try another PDF."\cf4 \strokec4 )\cb1 \
\pard\pardeftab720\partightenfactor0
\cf2 \cb3 \strokec2 else\cf4 \strokec4 :\cb1 \
\pard\pardeftab720\partightenfactor0
\cf4 \cb3     st.info(\cf6 \strokec6 "Upload a legal PDF file to begin."\cf4 \strokec4 )\cb1 \
}