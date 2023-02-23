const jwt = require('jsonwebtoken');
const UserRepo = require('./query');
const crypto = require('crypto');


/** 해당 id의 회원정보들 */
exports.info = async (ctx, next) => {
    let { userId } = ctx.state;

    let result = await UserRepo.findUserbyId(userId);

    ctx.body = {
        result : "ok",
        id : result.id,
        email : result.email,
        name : result.name
    };
}
/** 회원 가입 */
exports.register = async (ctx, next) => {
    let { email, password, name } = ctx.request.body;

    let checkEmail = await UserRepo.findUserbyEmail(email);
    if(checkEmail != null){
        ctx.body = {
            result : "이미 가입된 이메일입니다."
        }
        return;
    }

    let result = await crypto.pbkdf2Sync(password, process.env.APP_KEY, 50, 100, 'sha512');
    let { affectedRows, insertId } = await UserRepo.register(email, result.toString('base64'), name);

    if(affectedRows > 0){
        let token = await generteToken({ userId : insertId });
        ctx.body = token;
    } else{
        ctx.body = {result: "fail"};
    }
}
/** 로그인 */
exports.login = async (ctx, next) => {
    let { email, password } = ctx.request.body;
    let result = await crypto.pbkdf2Sync(password, process.env.APP_KEY, 50, 100, 'sha512');

    let item = await UserRepo.login(email, result.toString('base64'));

    if(item == null){
        ctx.body = {result: "fail"};
    } else {
        let token = await generteToken({ userId : item.id });
        ctx.body = token;
    }
}

/** 회원 탈퇴 */
exports.signOut = async (ctx, next) => {
    let { userId } = ctx.state;

    let { affectedRows } = await UserRepo.signOut(userId);

    if (affectedRows > 0){
        ctx.body = {result: "SignOut success"};
    } else {
        ctx.body = {result: "fail"};
    }
}

/**
 * jwt 토큰 생성
 * @param {object} payload 추가적으로 저장할 payload
 * @returns {string} jwt 토큰 string
 */
let generteToken = (payload) => {
    return new Promise((resolve, reject) => {
        jwt.sign(payload, process.env.APP_KEY, (error, token) => {
            if(error) { reject(error); }
            resolve(token);
        })
    })
}