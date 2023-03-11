const jwt = require('jsonwebtoken');
const PrintRepo = require('./query');
const crypto = require('crypto');
const { spawn } = require('child_process');
const path = require('path');


/** 해당 id의 회원의 인쇄 기록 */
exports.getPrintHistory = async (ctx, next) => {
    let { userId } = ctx.state;

    let result = await PrintRepo.getPrintHistory(userId);

    ctx.body = {
        result : result
    };
}

/** 해당 id의 인쇄 기록의 원문 가져오기 */
exports.getPrintContent = async (ctx, next) => {
    let { id } = ctx.request.body;

    let result = await PrintRepo.getPrintContent(id);

    console.log(result);

    ctx.body = {
        content : result[0].content
    };
}

/** 인쇄 문서 제출 */
exports.submitPrint = async (ctx, next) => {
    let { userId } = ctx.state;
    let { title, content, page } = ctx.request.body;

    let { affectedRows } = await PrintRepo.submitPrint(userId, title, content, page);

    if(affectedRows > 0){
        ctx.body = {
            result : "success Submit"
        };
    } else{
        ctx.body = {result: "fail"};
    }
}

/** 인쇄 문서 상태 변경 */
exports.setPrintState = async (ctx, next) => {
    let { userId } = ctx.state;
    let { id, state } = ctx.request.body;

    // 유저 정보 확인
    let doc = await PrintRepo.findPrintHistoryFromId(id);
    if( userId != doc.user_id ){
        ctx.body = {
            result : "유저 정보가 일치하지 않습니다."
        };
        return;
    }
    
    let { affectedRows } = await PrintRepo.setPrintState(id, state);

    if(affectedRows > 0){
        ctx.body = {
            result : "success State Update"
        };
    } else{
        ctx.body = {result: "fail"};
    }
}

/** 인쇄 문서 기록 삭제 */
exports.deletePrintHistory = async (ctx, next) => {
    let { userId } = ctx.state;
    let { id } = ctx.request.body;

    // 유저 정보 확인
    let doc = await PrintRepo.findPrintHistoryFromId(id);
    if( userId != doc.user_id ){
        ctx.body = {
            result : "유저 정보가 일치하지 않습니다."
        };
        return;
    }
    
    let { affectedRows } = await PrintRepo.deletePrintHistory(id);

    if(affectedRows > 0){
        ctx.body = {
            result : "success Delete"
        };
    } else{
        ctx.body = {result: "fail"};
    }
}

/** 점자 번역 결과 */
exports.getBrailleData = async (ctx, next) => {

    let { content } = ctx.request.body;

    console.log(path.join(__dirname, '../../braille/braillePrint.py'));

    const pythonProcess = spawn('python', [path.join(__dirname, '../../braille/braillePrint.py'), content]);

    let result = "";

    // 파이썬 출력 가져오기
    pythonProcess.stdout.on('data', (data) => {
        result += data.toString('utf-8');  // 버퍼 데이터를 문자열로 변환
    });

    // stdout의 end 이벤트를 사용하여 출력이 끝나기 전까지 대기
    await new Promise((resolve, reject) => {
        pythonProcess.stdout.on('end', () => {
        resolve();
        });
    });

    // HTTP 응답으로 전송
    ctx.body = {
        result: result
    };
  
}