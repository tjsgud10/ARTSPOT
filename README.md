# ARTSPOT

Seoul Art Exhibition Recommendation Platform

서울 전시 추천 서비스를 만들기 위한 **10주차 학습용 프로젝트 시작본**입니다. CSV를 읽고 날짜와 관람료로 전시를 골라 결과를 저장하는 과정을 GitHub Actions로 실행합니다.

> **모든 전시명, 전시장, 일정, 요금은 직접 만든 가상 예시입니다. 실제 전시 안내나 실시간 수집 결과가 아닙니다.** 현재 웹사이트나 AI 추천 모델은 구현하지 않았습니다.

## 목표와 범위

- CSV 데이터 검증 → 기간/예산 필터 → 가격순 추천 → CSV/JSON 저장
- 설치할 외부 Python 패키지, API 키, 유료 서비스 없이 실행
- GitHub Actions의 이벤트, 작업(job), 단계(step), 실행 환경(runner) 이해
- 완성된 기말 프로젝트가 아닌, 확장 가능한 작은 실습 결과물

## 파일별 역할

| 파일 | 역할 |
| --- | --- |
| `data/exhibitions.csv` | 가상 전시 5건과 `is_sample=true` 표시 |
| `scripts/process_exhibitions.py` | 데이터 검사, 추천, 결과 저장 |
| `.github/workflows/process-exhibitions.yml` | 버튼으로 실행하는 자동화 설정 |
| `.gitignore` | 결과물과 비밀 설정 파일 제외 |

## 내 컴퓨터에서 실행

Python 3.10 이상이 필요합니다. 저장소의 **Code → Download ZIP**으로 내려받고 압축을 푼 다음, 해당 폴더에서 실행합니다.

```bash
python scripts/process_exhibitions.py --as-of 2026-11-03 --max-price 10000
```

Windows에서 `python`이 인식되지 않으면 `py`로 바꿔 실행할 수 있습니다. 패키지 설치는 필요 없습니다.

- `results/recommendations.csv`: 추천 전시 목록
- `results/summary.json`: 기준 날짜, 건수, 추천 결과와 가상 데이터 안내
- 예상 결과: 전체 5건, 기간 내 3건, 1만 원 이하 추천 2건(`S001`, `S002`)
- 시작일과 종료일을 모두 포함합니다. 가격이 같으면 종료일, ID 순으로 정렬합니다.
- `--as-of`를 생략하면 컴퓨터의 오늘 날짜를 사용하므로 결과가 달라질 수 있습니다.
- 입력 열 누락, 빈 값, 중복 ID, 잘못된 날짜 범위, 음수 요금은 오류로 처리합니다.

## GitHub에서 버튼으로 실행

1. 저장소 상단의 **Actions**를 누릅니다.
2. **Process sample exhibitions**를 선택합니다.
3. **Run workflow → main → Run workflow**를 누릅니다.
4. 생성된 실행 기록을 열어 **Success**인지 확인합니다. 실패하면 빨간 단계의 로그를 읽습니다.
5. 실행 상세 화면의 **Artifacts**에서 `artspot-sample-results`를 내려받습니다.

워크플로는 고정 날짜 `2026-11-03`으로 실행하고 예상 건수와 ID를 검사합니다. 결과는 7일 보관하는 다운로드 파일(artifact)로 남깁니다. 저장소에 결과를 다시 커밋하지 않으므로 `contents: read` 권한만 사용합니다. 정기 실행은 설정하지 않았습니다.

## 수업 자료와 연결

- **GitHub Actions for Beginners**: 8~10쪽의 YAML 경로와 `workflow_dispatch`, 12~14쪽의 결과 보존과 최소 권한, 15~16쪽의 수동 실행과 로그 확인을 적용했습니다.
- **Lyric2Poster Design Specification (Open-Source Edition)**: 목표/범위 구분, 키 없이 동작하는 데모, 파일별 역할, 검증한 것과 미검증 항목을 구분하는 방식을 참고했습니다. 다른 프로젝트의 기능이나 코드는 복사하지 않았습니다.
- 이 구성은 두 자료를 ARTSPOT에 응용한 실습입니다. 교수자의 별도 과제 안내나 채점 기준을 대체하지 않습니다.

## 검증 상태

- 로컬 검증 완료(2026-11-03): 전체 5건, 기간 내 3건, 추천 2건과 추천 ID, 결과 CSV 저장, 중복 ID 거부를 확인했습니다.
- GitHub Actions 실제 실행 완료(2026-11-03): [수동 실행 #1 — Success](https://github.com/tjsgud10/ARTSPOT/actions/runs/41579724614), 총 13초, 결과 artifact 1개 생성. Python 처리 및 예상 결과 검사 단계가 통과했습니다.
- 실행에는 구버전 Action의 Node.js 20 사용 중단 경고가 표시됐으며 GitHub가 Node.js 24로 실행했습니다. 실행은 성공했습니다. 수업 예시 버전을 사용했으며, 다음 개선 때 [checkout](https://github.com/actions/checkout), [setup-python](https://github.com/actions/setup-python), [upload-artifact](https://github.com/actions/upload-artifact)의 최신 안내에 맞춰 갱신할 수 있습니다.
- 실제 전시 API 수집, 웹 배포, 개인화/AI 추천: 구현 및 검증하지 않았습니다.

## 앞으로 확장할 내용

1. 이용 조건을 확인한 공공 전시 데이터로 교체하고 출처/수집 시각 기록
2. 장르와 지역 필터 및 화면 추가
3. 수집 실패 시 기존 데이터 보존과 중복 수집 방지
4. 필요할 때만 정기 실행 추가(UTC와 한국 시간 차이 확인)

현재 코드에는 네트워크 호출과 API 키가 없습니다. 이후 키가 필요해지면 코드나 CSV에 넣지 않고 GitHub Repository secrets로 관리합니다.
