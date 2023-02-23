const jwt = require('jsonwebtoken');
const PrintRepo = require('./query');
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

/** 인쇄 문서 제출 */
exports.submitPrint = async (ctx, next) => {
    let { userId } = ctx.state;
    let { title, page } = ctx.request.body;

    let { affectedRows, insertId } = await PrintRepo.submitPrint(userId, title, page);

    if(affectedRows > 0){
        ctx.body = {
            result : "success Submit"
        };
    } else{
        ctx.body = {result: "fail"};
    }
}
