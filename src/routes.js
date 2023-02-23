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

router.post('/api/user/login', apiUserController.login);
router.post('/api/user/register', apiUserController.register);

router.use(verify)
router.get('/api/user/:id', apiUserController.info);

module.exports = router;