const Router = require('@koa/router');
const router = new Router();
const multer = require('@koa/multer');
const path = require('path');
const upload = multer({
    dest: path.resolve(__dirname, '../', 'storage')
});

const { myLogging } = require('./middleware/logging');
const { verify } = require('./middleware/auth');

const apiUserController = require('./api/user/controller');
const apiPrintController = require('./api/print/controller');

router.use(myLogging);

//메인
router.get('/', apiUserController.main);
//로그인
router.post('/api/user/login', apiUserController.login);
//회원가입
router.post('/api/user/register', apiUserController.register);

// 로그인 검증이 필요한 서비스 ↓↓↓
router.use(verify)  // 로그인 검증

// 유저 정보 검색
router.get('/api/user', apiUserController.info);
// 회원 탈퇴
router.delete('/api/user', apiUserController.signOut);

// 인쇄 문서 제출
router.post('/api/print', apiPrintController.submitPrint);
// 인쇄 문서 목록 불러오기
router.get('/api/print', apiPrintController.getPrintHistory);
// 인쇄 문서 원문 불러오기
router.get('/api/print/content', apiPrintController.getPrintContent);
// 인쇄 문서 상태 변경
router.put('/api/print', apiPrintController.setPrintState);
// 인쇄 문서 기록 삭제
router.delete('/api/print', apiPrintController.deletePrintHistory);

// 점역 결과
router.get('/api/braille', apiPrintController.getBrailleData);

module.exports = router;