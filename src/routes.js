const Router = require('@koa/router');
const router = new Router();
const multer = require('@koa/multer');
const path = require('path');
const upload = multer({
    dest: path.resolve(__dirname, '../', 'storage')
});

const { myLogging } = require('./middleware/logging');
const { verify } = require('./middleware/auth');

const webController = require('./web/controller');
const apiUserController = require('./api/user/controller');

router.use(myLogging);

router.get('/', webController.home);
router.get('/page/:page', webController.page);

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

module.exports = router;