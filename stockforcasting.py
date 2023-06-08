{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "```\n",
    "목차\n",
    "___\n",
    "Step 0. 패턴 검색\n",
    "Step 1. 코스피 종가 가져오기\n",
    "Step 2. 기준 구간 지정 및 시각화\n",
    "Step 3. 패턴 검색기 구현\n",
    "Step 4. 검색 구간 이후의 추세 확인\n",
    "```"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Step 0. 패턴 검색\n",
    "\n",
    "이번에는 현재 차트와 유사한 차트를 찾아서 매매에 활용하는 패턴 검색을 파이썬으로 구현해봅니다. 패턴 검색은 과거 주가에서 현재 주가와 유사한 패턴을 관측한 다음, 과거 주가 이후의 흐름을 확인하는 것을 통해 앞으로의 주가를 예상해보는 방식입니다."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Step 1. 코스피 종가 가져오기"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "2010년부터 오늘날짜까지의 데이터를 스크리닝할 것입니다. 즉, 유사한 패턴을 관측하는 가장 먼 시점은 2010년입니다."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [],
   "source": [
    "import FinanceDataReader as fdr\n",
    "import matplotlib.pyplot as plt\n",
    "\n",
    "import yfinance as yf\n",
    "from scipy.spatial.distance import cosine"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>Open</th>\n",
       "      <th>High</th>\n",
       "      <th>Low</th>\n",
       "      <th>Close</th>\n",
       "      <th>Volume</th>\n",
       "      <th>Dividends</th>\n",
       "      <th>Stock Splits</th>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Date</th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>2010-01-04</th>\n",
       "      <td>1681.709961</td>\n",
       "      <td>1696.140015</td>\n",
       "      <td>1681.709961</td>\n",
       "      <td>1696.140015</td>\n",
       "      <td>296500</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2010-01-05</th>\n",
       "      <td>1701.619995</td>\n",
       "      <td>1702.390015</td>\n",
       "      <td>1686.449951</td>\n",
       "      <td>1690.619995</td>\n",
       "      <td>408900</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2010-01-06</th>\n",
       "      <td>1697.880005</td>\n",
       "      <td>1706.890015</td>\n",
       "      <td>1696.099976</td>\n",
       "      <td>1705.319946</td>\n",
       "      <td>426000</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2010-01-07</th>\n",
       "      <td>1702.920044</td>\n",
       "      <td>1707.900024</td>\n",
       "      <td>1683.449951</td>\n",
       "      <td>1683.449951</td>\n",
       "      <td>462400</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2010-01-08</th>\n",
       "      <td>1694.060059</td>\n",
       "      <td>1695.260010</td>\n",
       "      <td>1668.839966</td>\n",
       "      <td>1695.260010</td>\n",
       "      <td>380000</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>...</th>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2022-06-08</th>\n",
       "      <td>2633.530029</td>\n",
       "      <td>2639.520020</td>\n",
       "      <td>2621.959961</td>\n",
       "      <td>2626.149902</td>\n",
       "      <td>576000</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2022-06-09</th>\n",
       "      <td>2618.919922</td>\n",
       "      <td>2627.879883</td>\n",
       "      <td>2606.610107</td>\n",
       "      <td>2625.439941</td>\n",
       "      <td>814500</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2022-06-10</th>\n",
       "      <td>2596.370117</td>\n",
       "      <td>2602.800049</td>\n",
       "      <td>2583.739990</td>\n",
       "      <td>2595.870117</td>\n",
       "      <td>723800</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2022-06-13</th>\n",
       "      <td>2550.209961</td>\n",
       "      <td>2550.320068</td>\n",
       "      <td>2504.510010</td>\n",
       "      <td>2504.510010</td>\n",
       "      <td>659800</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2022-06-14</th>\n",
       "      <td>2472.959961</td>\n",
       "      <td>2503.169922</td>\n",
       "      <td>2457.389893</td>\n",
       "      <td>2492.969971</td>\n",
       "      <td>671200</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "<p>3066 rows × 7 columns</p>\n",
       "</div>"
      ],
      "text/plain": [
       "                   Open         High          Low        Close  Volume  \\\n",
       "Date                                                                     \n",
       "2010-01-04  1681.709961  1696.140015  1681.709961  1696.140015  296500   \n",
       "2010-01-05  1701.619995  1702.390015  1686.449951  1690.619995  408900   \n",
       "2010-01-06  1697.880005  1706.890015  1696.099976  1705.319946  426000   \n",
       "2010-01-07  1702.920044  1707.900024  1683.449951  1683.449951  462400   \n",
       "2010-01-08  1694.060059  1695.260010  1668.839966  1695.260010  380000   \n",
       "...                 ...          ...          ...          ...     ...   \n",
       "2022-06-08  2633.530029  2639.520020  2621.959961  2626.149902  576000   \n",
       "2022-06-09  2618.919922  2627.879883  2606.610107  2625.439941  814500   \n",
       "2022-06-10  2596.370117  2602.800049  2583.739990  2595.870117  723800   \n",
       "2022-06-13  2550.209961  2550.320068  2504.510010  2504.510010  659800   \n",
       "2022-06-14  2472.959961  2503.169922  2457.389893  2492.969971  671200   \n",
       "\n",
       "            Dividends  Stock Splits  \n",
       "Date                                 \n",
       "2010-01-04          0             0  \n",
       "2010-01-05          0             0  \n",
       "2010-01-06          0             0  \n",
       "2010-01-07          0             0  \n",
       "2010-01-08          0             0  \n",
       "...               ...           ...  \n",
       "2022-06-08          0             0  \n",
       "2022-06-09          0             0  \n",
       "2022-06-10          0             0  \n",
       "2022-06-13          0             0  \n",
       "2022-06-14          0             0  \n",
       "\n",
       "[3066 rows x 7 columns]"
      ]
     },
     "execution_count": 2,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# 코스피 지수 추출\n",
    "kospi = yf.Ticker('^KS11').history(start='2010-01-01', end='2022-06-15')\n",
    "kospi"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Step 2. 기준 구간 지정 및 시각화"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "종가만 추출해서 검색하고자 하는 현재 주가의 패턴을 확인합니다. 여기서 현재 주가는 6월 2일까지만 확인합니다. 마지막에 6월 2일 이후 주가를 그려보면서 패턴 검색 방식의 예측을 검증해보기 위함입니다."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 종가만 추출\n",
    "kospi_close = kospi['Close']\n",
    "\n",
    "# 비교 기준 구간\n",
    "d_start = '2022-01-01'\n",
    "d_end = '2022-06-02'"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "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",
      "text/plain": [
       "<Figure size 864x288 with 1 Axes>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "# 기준 구간 시계열 차트\n",
    "plt.figure(figsize=(12,4))\n",
    "plt.style.use('seaborn')\n",
    "kospi_close[d_start:d_end].plot();"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "코스피는 올해 1월에 급락 후 횡보하는 모습을 보입니다. 이와 유사한 패턴을 과거에서 찾아봅니다."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Step 3. 패턴 검색기 구현"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "패턴 검색은 다음과 같은 로직으로 구성했습니다.\n",
    "\n",
    "1. 먼저 앞에서 지정한 기준 구간의 데이터가 있을 것입니다. \n",
    "2. 해당 데이터 길이만큼 최초 상장일부터 하루씩 비교하면서 코사인 유사도를 계산합니다. \n",
    "3. 단, 과거의 주가와 현재 주가의 액수 차이가 크기 때문에 패턴만 추출하기 위해서 표준화를 먼저 수행한 다음 데이터를 비교합니다.\n",
    "4. 이렇게 모든 데이터를 비교해서 코사인 유사도가 가장 작은 값 즉, 현재 주가 패턴과 가장 유사한 과거 시점의 주가를 찾습니다.\n",
    "\n",
    "이러한 흐름을 코드로 구현해보면 다음과 같습니다."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {},
   "outputs": [],
   "source": [
    "count = 0\n",
    "compare_base_r = kospi_close[d_start:d_end]\n",
    "# series에서 값만 추출\n",
    "compare_base = compare_base_r.values\n",
    "# 표준화\n",
    "compare_base_norm = (compare_base - compare_base.mean()) / compare_base.std()\n",
    "# array -> 1차원 리스트로 변환\n",
    "compare_base_norm = list(compare_base_norm)\n",
    "\n",
    "# 검색 기간\n",
    "window_size = len(compare_base_norm)\n",
    "# 검색 기간에 더해서 추가로 보여줄 기간\n",
    "next_date = 7\n",
    "# 검색 횟수\n",
    "moving_cnt = len(kospi_close) - 2*(window_size-1) - next_date\n",
    "\n",
    "# 유사도 저장 딕셔너리\n",
    "sim_dict = {}\n",
    "\n",
    "for i in range(moving_cnt):\n",
    "    compare_target_r = kospi_close[i:i+window_size]\n",
    "    # series에서 값만 추출\n",
    "    compare_target = compare_target_r.values\n",
    "    # 표준화\n",
    "    compare_target_norm = (compare_target - compare_target.mean()) / compare_target.std() \n",
    "    # array -> 1차원 리스트로 변환\n",
    "    compare_target_norm = list(compare_target_norm)\n",
    "\n",
    "    # 코사인 유사도 저장\n",
    "    sim = cosine(compare_base_norm, compare_target_norm)\n",
    "    # 코사인 유사도 <- i(인덱스), 시계열데이터 함께 저장\n",
    "    sim_dict[sim] = [i,compare_target_r]"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "이렇게 반복문을 통해 모든 코사인 유사도를 단일 리스트에 저장했다면, 이 값이 가장 작았던 구간을 추출해야 합니다. 반복문에서 인덱스를 함께 저장했기 때문에 간단하게 불러낼 수 있습니다."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "[1154,\n",
       " Date\n",
       " 2014-08-27    2074.929932\n",
       " 2014-08-28    2075.760010\n",
       " 2014-08-29    2068.540039\n",
       " 2014-09-01    2067.860107\n",
       " 2014-09-02    2051.580078\n",
       "                  ...     \n",
       " 2015-01-19    1902.619995\n",
       " 2015-01-20    1918.310059\n",
       " 2015-01-21    1921.229980\n",
       " 2015-01-22    1920.819946\n",
       " 2015-01-23    1936.089966\n",
       " Name: Close, Length: 100, dtype: float64]"
      ]
     },
     "execution_count": 6,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# 최소 코사인 유사도\n",
    "min_sim = min(list(sim_dict.keys()))\n",
    "# 최소 코사인 유사도가 나온 인덱스, 기간 추출\n",
    "sim_dict[min_sim]"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Step 4. 패턴 비교 시각화\n",
    "\n",
    "패턴이 유사한 시점을 찾았는데, 이때의 주가 패턴이 얼마나 현재 패턴과 유사한지 궁금합니다. 두 그래프를 동시에 그려보고 싶습니다. 두 시점의 주가 분포는 차이가 있기 때문에 그래프를 그리기 전에 표준화를 진행합니다."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "[2.8741732345009217,\n",
       " 2.4971152595282913,\n",
       " 2.139621933541546,\n",
       " 2.506949784258656,\n",
       " 2.205796174521818,\n",
       " 2.2128510366094445,\n",
       " 2.694998529560686,\n",
       " 2.583924254361606,\n",
       " 2.1544807311238086,\n",
       " 1.8143074439137883,\n",
       " 1.5378471564895781,\n",
       " 1.3030818087064449,\n",
       " 1.5211691806331475,\n",
       " 1.2176639502004345,\n",
       " 0.7655576938857375,\n",
       " 2.0619093758480324e-06,\n",
       " -0.11919718024448753,\n",
       " -1.1321323473770857,\n",
       " -0.6098950720855043,\n",
       " -0.13437700928689764,\n",
       " 0.3193317943166646,\n",
       " 0.2637411514737669,\n",
       " 0.2788139700294613,\n",
       " 0.5180711482427852,\n",
       " 0.5509964479969123,\n",
       " 0.29207022032285895,\n",
       " -0.17008458169563434,\n",
       " -0.4687795602498807,\n",
       " 0.09931823362907827,\n",
       " 0.25337157430982343,\n",
       " 0.25796780521485857,\n",
       " 0.2502708802069377,\n",
       " -0.14538864937113563,\n",
       " -0.00919039990069437,\n",
       " -0.7653369390816832,\n",
       " -0.4664279395540053,\n",
       " -0.2267453294056895,\n",
       " -0.18034714837286206,\n",
       " 0.28533638969537994,\n",
       " -0.07440415651239637,\n",
       " -0.7385034070347406,\n",
       " -1.0475705727648015,\n",
       " -0.42836874644939316,\n",
       " -0.6319183522539804,\n",
       " -0.7990139222546917,\n",
       " -1.0568700450615875,\n",
       " -0.6538346219357406,\n",
       " -0.27666963647639453,\n",
       " -0.14293001818854445,\n",
       " -0.3671117678343029,\n",
       " -0.11107221328970372,\n",
       " 0.1567280547461437,\n",
       " 0.09910421265564676,\n",
       " 0.10252593821867971,\n",
       " 0.09803671780036036,\n",
       " 0.2210857274641197,\n",
       " 0.28170064315891546,\n",
       " 0.3983342436434719,\n",
       " 0.20804349814415352,\n",
       " 0.4010068957994946,\n",
       " 0.4149052090131868,\n",
       " 0.1565140337727122,\n",
       " -0.2622362708291236,\n",
       " -0.2138101105724391,\n",
       " -0.2917424550320889,\n",
       " -0.5733340257949128,\n",
       " -0.041690267719829616,\n",
       " -0.03933864702395419,\n",
       " -0.26009867110667967,\n",
       " -0.29056794969008676,\n",
       " -0.016033851026760273,\n",
       " -0.018171450749204197,\n",
       " 0.0836033521530894,\n",
       " -0.16762595051304316,\n",
       " -0.6762859440510797,\n",
       " -0.5567630604251979,\n",
       " -0.8694633626798522,\n",
       " -0.5655300903002762,\n",
       " -0.2708962902174862,\n",
       " -0.35214595976532426,\n",
       " -0.42687320964724373,\n",
       " -0.4577679201656427,\n",
       " -0.8112000676809319,\n",
       " -1.323814229203709,\n",
       " -1.3696773578029577,\n",
       " -1.8207135092504971,\n",
       " -1.241711085774016,\n",
       " -1.3236002082302774,\n",
       " -1.06852374806612,\n",
       " -1.009297358686758,\n",
       " -1.3689282843959474,\n",
       " -0.8670047314972611,\n",
       " -0.7805193781359644,\n",
       " -1.224284036510575,\n",
       " -1.1029471946342677,\n",
       " -1.1539416065721302,\n",
       " -0.8802609817906587,\n",
       " -0.542332304789798,\n",
       " -0.3687169251350392,\n",
       " -0.6564002636050476]"
      ]
     },
     "execution_count": 7,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# 표준화된 기준 구간 데이터 \n",
    "compare_base_norm"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "[2.4477763309457883,\n",
       " 2.340917173477358,\n",
       " 2.155691134445625,\n",
       " 1.913060613229205,\n",
       " 1.7814754304013225,\n",
       " 1.3827515398793042,\n",
       " 1.0795959288832093,\n",
       " 1.2498776957148874,\n",
       " 0.593040975984155,\n",
       " 0.19184212081783542,\n",
       " 0.511123058192072,\n",
       " 1.028101966718636,\n",
       " 1.1195864233532198,\n",
       " 0.9230721309438193,\n",
       " 0.9807994346038496,\n",
       " 1.0914195934882758,\n",
       " 1.683542417954386,\n",
       " 1.7668566042414513,\n",
       " 1.4317731619644165,\n",
       " 1.702785727362676,\n",
       " 1.7271889312467843,\n",
       " 1.556151289741131,\n",
       " 1.2935242090072858,\n",
       " 0.7743957818766045,\n",
       " 0.8932938182669973,\n",
       " 0.9158703250223316,\n",
       " 1.141302072840971,\n",
       " 1.190428677519691,\n",
       " 0.9398431002726483,\n",
       " 1.0518595276520568,\n",
       " 0.9128599491506311,\n",
       " 0.8877034951573876,\n",
       " 0.9780042730490447,\n",
       " 0.5940068158453458,\n",
       " 0.18926217357992636,\n",
       " 0.2811770588483018,\n",
       " -0.25246521184864307,\n",
       " -0.8653352213764737,\n",
       " -1.4443404707713028,\n",
       " -0.8944678911026085,\n",
       " -0.9284376338292177,\n",
       " -1.3575881045435856,\n",
       " -1.0562591906762644,\n",
       " -0.5807772768379815,\n",
       " -0.2967547435268886,\n",
       " -0.38684293166649014,\n",
       " -0.14646691164779557,\n",
       " -0.31750455315344905,\n",
       " -0.379853715497058,\n",
       " -0.3924332547760998,\n",
       " -0.2378437611239316,\n",
       " 0.06896786869455131,\n",
       " -0.1846307089890322,\n",
       " -0.35598854740518915,\n",
       " -0.7738507647418897,\n",
       " -0.6850538625036627,\n",
       " -0.3136333200141654,\n",
       " -0.7197768553394073,\n",
       " -0.6390426162902512,\n",
       " -0.7890076266940005,\n",
       " -0.8865128350719855,\n",
       " -0.8622172383463251,\n",
       " -1.2093421841101621,\n",
       " -1.265780826433658,\n",
       " -0.7940599140113707,\n",
       " -0.46381354473481046,\n",
       " -0.4886471772527103,\n",
       " -0.8626476669801167,\n",
       " -1.0243313593953247,\n",
       " -0.7701947459195019,\n",
       " -0.31621326725207444,\n",
       " -0.48735589135133567,\n",
       " -0.5200369727414105,\n",
       " -0.670755233254295,\n",
       " -1.1419381098843429,\n",
       " -1.433482646027427,\n",
       " -2.189331074354415,\n",
       " -1.5366857846734696,\n",
       " -1.047012848744267,\n",
       " -0.799112201328741,\n",
       " -0.7462219706691852,\n",
       " -0.547665766814115,\n",
       " -0.43930273369225437,\n",
       " -0.14076898137973803,\n",
       " -0.34867913432525355,\n",
       " -0.44080923391052473,\n",
       " -0.588194297076365,\n",
       " -0.5727146136489106,\n",
       " -0.3897457003797429,\n",
       " -0.26805250243454526,\n",
       " -0.8564117009198198,\n",
       " -0.7270862684193429,\n",
       " -0.6254972371500185,\n",
       " -0.478327388301074,\n",
       " -0.32502918055028046,\n",
       " -0.46349072325946683,\n",
       " -0.24106935131252796,\n",
       " -0.5307871903268383,\n",
       " -0.698922063119239,\n",
       " -0.5743260964607888]"
      ]
     },
     "execution_count": 8,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# 검색 구간 데이터 -> 값만 추출\n",
    "compare_target = compare_target_r.values\n",
    "# 검색 구간 데이터 표준화\n",
    "compare_target_norm = (compare_target - compare_target.mean())/compare_target.std()\n",
    "compare_target_norm = list(compare_target_norm)\n",
    "\n",
    "# 표준화된 검색 구간 데이터\n",
    "compare_target_norm"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "데이터간 범위를 맞춰줬으니 그래프를 그려봅니다."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "iVBORw0KGgoAAAANSUhEUgAAAwoAAAEFCAYAAABD8RDdAAAAOXRFWHRTb2Z0d2FyZQBNYXRwbG90bGliIHZlcnNpb24zLjMuNCwgaHR0cHM6Ly9tYXRwbG90bGliLm9yZy8QVMy6AAAACXBIWXMAAAsTAAALEwEAmpwYAABlBklEQVR4nO3deZhcVZ0//ve5S1V1dfWWpDshIYEEEsIyUUEBEVBxGxfMF7/i8hvJCCoiIjLKkkBARwJx+bo7oqgjEFRcxoD4OKMMy4jDKhAgkED2pdN7V9dedevee35/3N67uvrWdquq+/16njw03VX3nFvr+dzz+ZwjpJQSRERERERE4yjV7gAREREREdUeBgpERERERDQFAwUiIiIiIpqCgQIREREREU3BQIGIiIiIiKbQqt2BmfT1xarSbltbEOFwkm3P8nbZNp9rtj372mXbfK7Z9uxr1wvt7U3V7kLN4YzCNDRNZdtzoF22PXfaZdtzp122PXfaZdtzp12qDgYKREREREQ0heepR5ZlYePGjdi3bx9UVcXmzZuxbNkyr7tBRERERER5eD6j8PDDDwMA7rnnHlx55ZXYvHmz110gIiIiIqIZCCml9LpR0zShaRq2bt2KZ599FjfffHOe21rMhyMiIiIi8lhVVj3SNA3XXXcdHnjgAXzve9/Le9tqVda3tzdVbcWludj2XDznudr2XDznudr2XDznudr2XDznudp2Nc+50rjq0VRVK2b+2te+hj//+c+48cYbkUzOzmW2iIiIiIjqleczCvfeey96enrw6U9/Gg0NDRBCQFWZWkREREREtUFKoNzXsYNBQIjyHrPSPA8U3vnOd2LDhg34p3/6J5imieuvvx5+v9/rbhARERER5ZRMAlu3AuUaomYywAUXAI2N5TmeVzwPFILBIL773e963WzB4vFq94CIiIiIqsXvBwIBb9v8/e9/j7179+Lqq6/2tuFpcMO1abz8MhCbnbU6REREREQzqsqqR/VA14HduxW87nV2tbtCRERERHPEtm3b8M///M+Ix+P43Oc+h3Q6jV/84hejfx/JzLnqqqsgpUQ2m8W//uu/4oQTTsCWLVvwxz/+EUIIvOc978G6detK6gsDhTy6uwUsC2CtNRERERF5oaGhAbfffjsGBwdx4YUX4kMf+hBuv/12NDQ04KabbsLf/vY3NDc3o6mpCd/8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Ccccc4xn7f+f//N/0NTUBAA4+uijsXnz5oq29/zzz+P//b//hy1btuDAgQNYv349hBBYuXIlvvSlL0FRKhdLjm/7pZdewmWXXYZjjz0WAPDRj34U73nPe8reZjabxfXXX4/Ozk4YhoHPfOYzOP744z0571xtL1q0qOLnbVkWNm7ciH379kFVVWzevBlSSk/OOVfbsVjMk+d6xMDAAD7wgQ/g3//936Fpmmev8fHtptNpz8558mfIZZdd5tk5T277Yx/7mGfn/eMf/xgPPfQQstksPvrRj+L000/37Lwnt33SSSdV/Lx///vfY+vWrQCATCaDHTt24Je//CVuvfXWip9zrrbvuecezz7D169fj87OTiiKgptvvtmz93Wutr14bxuGgQ0bNuDQoUMIhUK46aabIITw5JxztZ1IJDz9DKcqkzTBn//8Z3nddddJKaV87rnn5GWXXeZZ2+l0Wq5du9az9m6//Xb5vve9T1544YVSSik//elPyyeeeEJKKeWNN94o//KXv3jW9m9+8xv5s5/9rGLtjfjd734nN23aJKWUcnBwUL75zW/27Lxzte3FeT/wwANy/fr1Ukopn3jiCXnZZZd5ds652vbquZZSSsMw5OWXXy7f+c53yt27d3t23pPb9eqcc32GeHXOudr26ryfeOIJ+elPf1paliXj8bj83ve+59l552rby9e4lFJ++ctflvfcc4+nn+GT2/bqnB944AF55ZVXSiml/Nvf/iavuOIKTz/PJrftxXlv2bJFbty4UUop5Z49e+Qll1zi2Tnnatvr1zdVF1OPJnnmmWdwzjnnAABe+9rXYvv27Z61vXPnTqRSKVxyySVYt24dtm3bVtH2li1bhu9///uj///SSy/h9NNPBwCce+65eOyxxzxre/v27XjkkUfwT//0T7j++usRj8cr0u4//uM/4vOf//zo/6uq6tl552rbi/N++9vfjptvvhkAcOTIESxYsMCzc87VtlfPNQB87Wtfw0c+8hF0dHQA8O41Prldr84512eIV+ecq22vzvtvf/sbVq1ahc9+9rO47LLL8Ja3vMWz887Vtpev8RdffBG7d+/Ghz/8YU8/wye37dU5L1++HJZlwbZtxONxaJrm2XnnatuL8969ezfOPfdcAMCKFSuwZ88ez845V9tevr6p+hgoTBKPxxEKhUb/X1VVmKbpSduBQACf+MQn8LOf/Qz/+q//iquvvrqibb/rXe+Cpo1ln0kpIYQAADQ2NiIWi3nW9po1a3DttdfiF7/4BZYuXYp/+7d/q0i7jY2NCIVCiMfjuPLKK3HVVVd5dt652vbqvDVNw3XXXYebb74Z73rXuzx9rie37dU5//73v8e8efNGA3/Am9d4rna9OudcnyFePde52j755JM9Oe9wOIzt27fju9/9rufnnattr55vwEl7+uxnPwvA28/wyW17dc7BYBCdnZ1497vfjRtvvBEXXXSRZ+edq20vzvvEE0/Eww8/DCkltm3bhp6eHs/OOVfbp5xyimevb6o+BgqThEIhJBKJ0f+3bXvCgLaSli9fjve///0QQmD58uVobW1FX1+fJ20DmJDfmEgk0Nzc7Fnb73jHO3DKKaeM/vzyyy9XrK2uri6sW7cOa9euxfnnn+/peU9u28vz/trXvoY///nPuPHGG5HJZEZ/78VzPb7ts88+25Nz/o//+A889thjuOiii7Bjxw5cd911GBwcHP17pc47V7vnnnuuJ+ec6zNkYGBg9O+VfK5ztX3OOed4ct6tra04++yz4fP5sGLFCvj9/gkDp0qed6623/KWt3hy3tFoFHv37sWZZ54JwNvP8Mlte/VZdscdd+Dss8/Gn//8Z9x3331Yv349stns6N8red652vbivf1//+//RSgUwrp16/Dwww/j5JNP9uy5ztX2u971Ls++t6j6GChMcuqpp+Kvf/0rAGDbtm1YtWqVZ23/7ne/w1e/+lUAQE9PD+LxONrb2z1r/6STTsKTTz4JAPjrX/+K17/+9Z61/YlPfAIvvPACAODxxx/HySefXJF2+vv7cckll+Caa67BBz/4QQDenXeutr0473vvvRc//vGPAQANDQ0QQuCUU07x5JxztX3FFVd48lz/4he/wN13340tW7bgxBNPxNe+9jWce+65FT/vXO1efvnlnpxzrs+QN73pTZ4817na/uxnP+vJeZ922ml49NFHIaVET08PUqkU3vjGN3py3rnavvTSSz0576effhpnnXXW6P97+Rk+uW2vPsObm5tHC+ZbWlpgmqZn552r7csuu6zi5/3iiy/itNNOw5YtW/D2t78dS5cu9eycc7Xt1XNNtUFIKWW1O1FLRlY9evXVVyGlxK233orjjjvOk7ZHVhc4cuQIhBC4+uqrceqpp1a0zcOHD+MLX/gCfvOb32Dfvn248cYbkc1msWLFCmzatAmqqnrS9ksvvYSbb74Zuq5jwYIFuPnmmyekgJXLpk2b8J//+Z9YsWLF6O9uuOEGbNq0qeLnnavtq666Ct/4xjcqet7JZBIbNmxAf38/TNPEpz71KRx33HGePNe52j7qqKM8ea7Hu+iii/DlL38ZiqJ4+hofaTedTntyzrk+Q9ra2jw551xt+/1+z57rr3/963jyySchpcS//Mu/4Oijj/bsuZ7c9rx58zw575/+9KfQNA0f//jHAcDTz/DJbXv1GZ5IJHD99dejr68P2WwW69atwymnnOLJeedqe8WKFRU/78HBQXzhC19AKpVCU1MTbrnlFiSTSU/OOVfb/f39nn+GU/UwUCAiIiIioimYekRERERERFMwUCAiIiIioikYKBARERER0RQMFIiIiIiIaAoGCkRERERENAUDBSKiGvPiiy/ihhtuKOg+J5xwwujP3d3d2LBhQ7m7ldOGDRvQ2dkJALj22mvR09PjSbtERFR5DBSIiGrMP/zDP+CWW24p+v633norPvnJT5axR9Mb2T8AAC699FLceuutnrRLRESVp1W7A0REs9GTTz6JH/7wh9A0DYcPH8aaNWtwyy234E9/+hPuvPNO2LaNk08+GV/60pfg9/tx5pln4pRTTkFfXx+uvfZa/OhHP8KWLVuwb98+3HTTTRgaGkIwGMQNN9yANWvW4PDhw7jmmmuQTCbxmte8ZrTdgwcPore3d3SjyMceewxf/epXIaXE4sWL8c1vfhPBYBC33norHn/8cQgh8P73vx+XXnopnnzySfzgBz/Ali1bAADr16/H6aefjtNPPx1XXHEFVq5ciR07dmD+/Pn47ne/i9/85jfo7e3FpZdeil/84hc4/vjj0dnZiYMHD2LZsmVVedyJiKh8OKNARFQhzz33HG644Qb813/9FzKZDH72s5/hN7/5De655x7cd999mD9/Pn72s58BAMLhMD71qU/hvvvug6aNXcO55pprcNFFF+H+++/Hhg0b8PnPfx6GYeDmm2/GBz7wAdx3330TdnB/6KGHRv/fMAxcffXV+NrXvob7778fq1atwtatW/GrX/0KXV1d+MMf/oDf/va3+Mtf/oJHHnkk77ns3LkTF198Mf74xz+iubkZ999/Py699FJ0dHTg9ttvR1tbGwDgtNNOw8MPP1zmR5KIiKqBgQIRUYW84Q1vwIoVKyCEwNq1a/H9738fBw4cwIc+9CGsXbsWDz74IPbu3Tt6+/EzAwCQSCRw8OBBvPOd7wQAvPa1r0VLSwv27t2Lp556Cu9+97sBAO9///uh6zoA4MCBA1i0aBEA4JVXXsHChQtx4oknAgC++MUv4qKLLsKTTz6JCy64AKqqoqGhAeeffz4ef/zxvOcyf/58nHTSSQCAlStXIhKJ5Lzd4sWLceDAgUIfKiIiqkFMPSIiqhBVVUd/llLCsiy8+93vxsaNGwE4gYBlWaO3CQQCE+4/kvs/+Xcj9xn5uxACiqKM/jwyI6HrOoQQo/eNxWJIJBKwbTvnMYUQE9rMZrOjP/v9/tGfJ99uPE3TRvtCRET1jZ/mREQV8swzz6Cnpwe2bePee+/F9ddfjwceeAADAwOQUuLLX/4y7rzzzmnvHwqFcPTRR+Mvf/kLAGDbtm3o7+/HypUrcdZZZ+EPf/gDAOAvf/kLMpkMAGDZsmWjqxAtX74cAwMD2L17NwDgpz/9KX71q1/hzDPPxL333gvLspBKpXD//ffjjDPOQFtbGw4dOoRMJoOhoSE888wzM56jqqoTgp3Dhw+zPoGIaJbgjAIRUYV0dHSMLhn6pje9CR/72McQDAbxz//8z7BtGyeeeCIuvfTSvMf4xje+gS9/+cv4/ve/D13X8f3vfx8+nw833XQTrrnmGvz617/GKaecgsbGRgDAW9/6Vlx99dUAnFmAb3zjG7j22muRzWaxbNkyfP3rX4fP58P+/fuxdu1aZLNZnH/++XjHO94BAHjzm9+M9773vViyZAlOO+20Gc/xLW95Cy699FL89Kc/xdKlS/H000/j29/+domPHBER1QIhp5s/JiKiok1eQchLV1xxBa688kqsWrXK03Z37tyJH/7wh/je977nabtERFQZTD0iIpplNmzYMLqakpd+8pOfYP369Z63S0RElcEZBSIiIiIimoIzCkRERERENAUDBSIiIiIimoKBAhERERERTcFAgYiIiIiIpmCgQEREREREU/z/0KcgAsEIUJEAAAAASUVORK5CYII=",
      "text/plain": [
       "<Figure size 864x288 with 1 Axes>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "import numpy as np\n",
    "\n",
    "xrange = np.arange(0, len(compare_base_norm),1)\n",
    "plt.figure(figsize=(12,4))\n",
    "plt.fill_between(x=xrange,\n",
    "                 y1=np.min(compare_base_norm), y2=compare_base_norm, \n",
    "                 label='base', alpha=0.3, color='blue')\n",
    "plt.fill_between(x=xrange,\n",
    "                 y1=np.min(compare_base_norm), y2=compare_target_norm, \n",
    "                 label='target', alpha=0.5, color='pink')\n",
    "plt.legend(bbox_to_anchor=(1.1, 1))\n",
    "plt.xticks(xrange[::5])\n",
    "plt.xlabel('period(count)')\n",
    "plt.ylabel('revenue(normalized)')\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "target(과거)도 base(현재)와 유사하게 급락 후 횡보하는 구간을 겪고 있습니다."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Step 4. 검색 구간 이후의 추세 확인\n",
    "이번에는 검색된 과거 주가 이후 7일간의 데이터와 6월 2일 이후 주가를 비교해보려 합니다. 패턴 검색 방식의 예측이 유효하다면 두 기간 이후 발생하는 추세도 유사할 것입니다."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "iVBORw0KGgoAAAANSUhEUgAAA1gAAAEYCAYAAABBWFftAAAAOXRFWHRTb2Z0d2FyZQBNYXRwbG90bGliIHZlcnNpb24zLjMuNCwgaHR0cHM6Ly9tYXRwbG90bGliLm9yZy8QVMy6AAAACXBIWXMAAAsTAAALEwEAmpwYAACNSklEQVR4nOzdd3hUddbA8e/U9N5JJSSht4B0qSqIFFFUxLWjriKWFVZ31XXXjn0t6ItlXRUFFBdURKWDdELoJCEB0nvPJJl63z8GRiMthCSTkPN5zBMyuXPn3PHkzj3311SKoigIIYQQQgghhLhoamcHIIQQQgghhBCXCimwhBBCCCGEEKKZSIElhBBCCCGEEM1ECiwhhBBCCCGEaCZSYAkhhBBCCCFEM5ECSwghhBBCCCGaiRRYQgjRzuzYsYNJkyY12/66du1KWVnZaY+/++67rFmzpsn7/frrr1m0aJHjZ6vVyn333UdJSQk2m41XXnmFa665hsmTJ/Pggw86YigrK2PWrFlMnDiRSZMmsWfPngb7VRSFxx9/nI8//viMr/vggw/y7LPPnjWuEydOcMsttzBx4kSmT59ORkaG43dz5szhyiuvZOrUqUydOpUXX3yxyccPsH//fmbMmMHUqVOZPHkyK1ascPzum2++YeLEiVx11VU888wzmM3mBs9NSUlhxIgRDR77/PPPGT58uCO+mTNnnvW1/+///o8JEyZw5ZVX8s4773BqVZbMzEzuvPNOpk6dysSJE/nkk08AqKmpYdasWdTX11/UMQshREcnBZYQQogz2rFjBxaLpcnPT0pKanCx/sknnzBo0CACAwNZtmwZhw4d4n//+x/ff/89UVFRvPzyywD861//YuDAgfz444+8+uqrPPzww9TV1QGQkZHB7bffzs8//3zG1/zwww/ZvXv3OeOaO3cuM2bM4Mcff2TOnDk8/PDDjuIjOTmZL774ghUrVrBixQr+/ve/N/n4FUXhoYce4qGHHmLFihV8+OGHvPzyy5w4cYK0tDTeeecdvvjiC3766Seqq6v59NNPAbBYLHz66afcfffdGAyGBvtMTk7miSeecMT35ZdfnvG1N27cyKpVq/j222/54Ycf2LFjB6tWrQLgiSeeYOLEiaxYsYIlS5awZMkStm3bhqenJ5MmTeLf//53k49ZCCGEFFhCCNEu1dbW8tBDDzF16lRuvfVWjh8/DsDx48e58847ufHGGxkzZgz3338/RqMRgH379nHDDTcwadIkpk2bxrZt2xrss7i4mEmTJrFo0SIWLVrEwYMHeeWVV1i9ejUmk4kXX3yRadOmMWXKFJ544glqamoA+PLLL5kyZQrXX389M2fOJD09ndWrV7Nu3To+/fRTFi1aRF1dHf/973+57rrrAIiLi+Ovf/0rer0egF69epGXl4fFYmHDhg3ceOONAHTv3p2YmBg2b94MwKJFi7jhhhuYMGHCae/Jjh072Lx5MzNmzDjr+1ZYWMixY8e45pprABg1ahS1tbUcPnyY7OxsDAYDTz/9NJMnT+Zvf/sbFRUVTf1fhMlkYvbs2QwbNgyA0NBQ/P39KSgoYO3atYwdOxZ/f3/UajU33XQT3333HQCHDx8mNTWVd99997R9Jicn8/333zN58mTuvvtuUlNTz/jaq1evZtKkSbi7u+Pi4sJ1113n2P/06dMdLaBeXl5ERUWRl5cHwNVXX833339PSUlJk49bCCE6OimwhBCiHcrPz+eOO+5gxYoVTJo0ib/+9a8ALF26lGuvvZalS5fyyy+/kJOTw4YNGzCbzcyePZvZs2fzww8/8Nxzz/Hiiy9is9kAe+Fxxx13cO+993LLLbdwyy230KtXL/76179y5ZVXsnDhQjQaDd9++y3fffcdwcHBvPbaa1itVl588UU++ugjli1bxo033khSUhJXXnklY8eO5Y477uCWW25h+/btdO7cGT8/PwD69+9Pz549AaisrGTBggVMmDCB8vJybDYb/v7+jmMNCQmhoKAAgH/84x9Mnjz5tPejsLCQF154gddeew2NRnPO9y04OBi1+rePv1P7LysrY9iwYfzrX/9i+fLluLu7n7EFa/v27dx0001ce+21vPnmm6Snp7NmzRo2btzYYDsXFxduuOEGx89LlizBYDDQr18/8vPzCQsLc/wuNDSUwsJCAPr06cNLL71EUFBQg/3V1tYSGxvLPffcw/fff8/111/PPffcc1or16njPNv+r7/+etzc3ADYtGkTycnJXH755Y6Ye/XqddqxCCGEaDytswMQQghx4bp27UpiYiIA06ZN45///CfV1dXMmzePLVu28OGHH3LixAmKioqora0lLS0NtVrN6NGjAXuL0ffff+/Y3z333ENoaOgZixeADRs2UF1dzdatWwEwm80EBASg0WiYMGECM2bMYPTo0YwYMYJRo0ad9vxjx44RFRV12uNZWVnMnj2bxMREbrnlFoqKilCpVA22URTlnEWT2Wzmscce429/+xvBwcHnfN9sNttZ99+3b1/ee+89x+MPPvggI0aMwGQyOVraAAoKCvjoo4+wWCz85z//Yfbs2cTFxfHcc8+d9XUXLlzIZ599xkcffYSrq6ujS+LvY/h90Xcm7u7uDcadTZw4kffff58DBw4wZMiQ0/b3++M80/6XL1/OSy+9xNtvv93gfYuIiHC0iAohhLhwUmAJIUQ79MeLZZVKhVar5S9/+QtWq5Wrr76a0aNHk5+f7ygg/lhYpKWlERsbC8Czzz7LBx98wH/+8x/uuuuu017PZrPx97//3VE8GQwGR9fD1157jbS0NLZu3crChQtZsWLFaeN4VCqVo7XslO3bt/Poo48ya9Ys7r77bgACAgJQFIWKigp8fX0BKCoqIiQk5KzvxcGDB8nOznaM4SopKcFqtWI0Ghk7dixvv/02AMHBwTz33HMUFxc3KECKiooIDQ1l9+7dVFZWMm7cOOC3IuWPxd21117r+Pdf/vIX/vKXv5w1NpPJxBNPPEF6ejqLFy8mIiICgLCwMIqKihzbnYrhXHJzc1m3bh233nqr4zFFUdBqtdxzzz2O/T300EPn3L+iKMyfP5+ff/6ZTz/9lO7duzd4HZ1Od86CVgghxLlJF0EhhGiHUlNTOXLkCGDvejZgwADc3Nz49ddfmT17NhMnTgTs466sViuxsbGoVCq2bNkCwKFDh7j99tsdRU+/fv14+eWXef/990lLSwNAo9E4JrkYMWIEixYtwmQyYbPZePrpp3njjTcoKytj1KhR+Pr6cscdd/DII49w4MCB057fuXNnsrOzHfEfOnSIBx98kPnz5zuKKwCtVsvo0aNZunQpYJ9JLyMjg8GDB5/1vejfvz8bN250TPwwY8YMJk6cyAsvvMC4ceMcj3/44YeEhoYSFRXFjz/+CMDmzZtRq9UkJCRgMBh4/vnnHeOuPv74Y8aPH39RxcbcuXOpqalpUFwBjB07lnXr1lFaWoqiKCxZsoQrrrjinPtyc3PjrbfeYv/+/YB9Iou6ujr69OnDhx9+6DjOcePGMW7cOL777jtqa2sxmUx8++23jv2/8sor7Nq1i2XLlp1WXAHk5OTQuXPnJh+zEEJ0dNKCJYQQ7VBsbCzvvvsu2dnZBAQEOFpvHn30UWbPno27uzuenp5cdtllZGVlodfreeedd3jxxRd55ZVX0Ol0vPPOOw26vsXGxvLAAw8wb948vv76a8aOHcsbb7yB2WzmgQceYP78+UybNg2r1Ur37t154okn8PT05P777+eOO+7A1dUVjUbD888/D8DIkSMdcd1xxx08+eSTVFVV4e3tzRtvvIGiKLz++uu8/vrrgL1r2nvvvcczzzzDU089xaRJk1CpVLzyyit4eXk123v3xhtv8PTTT/P++++j1+v597//jVqtZtSoUdx6663cfPPN2Gw2unbtes5uf+eTnJzMzz//TExMDDfffLPj8blz53L55Zcze/Zsbr/9dsxmM3379uWee+455/78/f156623+Mc//oHZbMbT05P33nuvwf/DU8aOHUtaWho33HADZrOZcePGce2111JQUMCnn35KWFgYd955p2P72267jeuvvx6TycTevXt54YUXmnzcQgjR0amUP3YEF0IIIVrABx98gEajOW8hIZzn22+/5ejRozz++OPODkUIIdot6SIohBCiVdx1111s376d4uJiZ4cizsBgMPDDDz8wZ84cZ4cihBDtmrRgCSGEEEIIIUQzkRYsIYQQQgghhGgmUmAJIYQQQgghRDNpk7MIFhdXOzuEVuXn5055ea2zwxBtnOSJaCrJHdFYkiuiqSR32h7/Ab0wGutZ/8lnzg7lnNzcdNTVmc+73aBBw1ohmgsTFHTmGW6lBasN0GplQUdxfpInoqkkd0RjSa6IppLcEU2lVl965UibbMFqayoNJsqr66mrt1BnslJntOCi09A3LhCd9tJLCiGEEEII0b6Vr91M0p6dzg6jQ5IC6zzKqup5/INtWG2nT7bo5+XCxCHRXN4nDL1O7twIIYQQQoi2QfH1w+LZfIu0i8aTAus8fDz1TBwSjdFsxc1Fa//Sa8gtMbAhOZdFq9P4YesJxg+Kom9cABqNGo1KhVqtQqM+83e1SuXswxJCCCGEEJcwdV4uriXF1AcGOTuUDkcKrPPQqNVMGxl7xt9NHBLNz7uyWLcnl6Xr01m6Pr1R+1SBo+DSatRMGxPHuH6dmjFqIYQQQgjRkflOHs/QdjDJxaVICqyL4O2h54bRcVw9OJoNybmUVNZhtSnYbIr9uwK23/9sszl+b1PAalMoqaxj0U8p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",
      "text/plain": [
       "<Figure size 864x288 with 2 Axes>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "# 반복문 인덱스 복원\n",
    "idx = sim_dict[min_sim][0]\n",
    "# 반복문 타겟 구간 시계열 데이터 복원\n",
    "compare_target_r = sim_dict[min_sim][1]\n",
    "\n",
    "plt.figure(figsize=(12,4))\n",
    "expanded_target_r = kospi_close[idx:idx+window_size+next_date]\n",
    "plt.subplot(211)\n",
    "expanded_target_r.plot()\n",
    "plt.axvspan(compare_target_r.index[-1], expanded_target_r.index[-1], facecolor='gray', alpha=0.5)\n",
    "plt.axvline(x=compare_target_r.index[-1], c='r', linestyle='--')\n",
    "plt.title('backtest(2014-05 ~ 2015-02)')\n",
    "\n",
    "plt.subplot(212)\n",
    "loc = kospi_close.index.get_loc(kospi_close.loc[d_start:].index[0])\n",
    "expanded_real_r = kospi_close[loc:loc+window_size+next_date]\n",
    "expanded_real_r.plot()\n",
    "plt.axvspan(expanded_real_r.index[-next_date], expanded_real_r.index[-1], facecolor='pink', alpha=0.5)\n",
    "plt.axvline(x=expanded_real_r.index[-next_date], c='r', linestyle='--')\n",
    "plt.title('real(2022-01 ~ 2022-06)')\n",
    "\n",
    "plt.tight_layout()\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "아쉽게도 2015년 2월 주가는 반등했지만 6월 주가는 다시 급락하고 있습니다. 이를 통해 가장 유사한 패턴 하나만 가지고 예측하는 것이 바람직하지 않다는 것을 알 수 있습니다. ​\n",
    "\n",
    "주가 움직임은 확률적으로 접근해야 합니다. 만약 패턴 검색 방식으로 주가를 예측하고자 한다면 유사한 패턴(표본)을 최대한 많이(최소 30개) 추출한 다음 상승 확률을 계산하는 것이 좋습니다. 물론 이를 위해서는 코스피 뿐만 아니라 전 세계 주가 데이터를 대상으로 스크리닝해야 충분한 표본을 확보할 수 있겠습니다."
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3.7.7 ('dataScience')",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.7"
  },
  "orig_nbformat": 4,
  "vscode": {
   "interpreter": {
    "hash": "946e70462398da2b7d5146f365841ff0dae0fe6e2f7c4e5ed0a8dd78c4677798"
   }
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}