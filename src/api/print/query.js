const { pool } = require('../../data');

/**
 * 인쇄 문서 제출 시
 * @param {Int} user_id 인쇄하는 회원의 유저ID
 * @param {string} title 문서의 간단한 타이틀
 * @param {Int} page 페이지 수
 * @returns 
 */
exports.submitPrint = async (user_id, title, page) => {
    const query = `INSERT INTO print
    (user_id, title, page)
    VALUES (?,?,?)`;
    return await pool(query, [user_id, title, page]);
}

/**
 * 해당 유저의 인쇄 기록을 불러오기
 * @param {Int} user_id 
 * @returns 
 */
exports.getPrintHistory = async (user_id) => {
    const query = `select * from print where user_id = ?`;
    let result = await pool(query, [user_id]);
    return (result.length < 0) ? null : result
}

/**
 * 인쇄 번호로 해당 문서의 인쇄 상태 갱신
 * @param {Int} id 문서 id
 * @param {string} state 문서 상태
 * @returns 
 */
exports.setPrintState = async (id, state) => {
    const query = `update print set state = ? where id = ?;`;
    return await pool(query, [state, id]);
}

/**
 * 문서 아이디로 해당 문서 찾기
 * @param {Int} id 문서 아이디
 * @returns 
 */
exports.findPrintHistoryFromId = async (id) => {
    const query = `select * from print where id = ?;`;
    let result = await pool(query, [id]);
    return (result.length < 0) ? null : result[0]
}

/**
 * 문서 아이디로 해당 문서 기록 삭제
 * @param {Int} id 문서 아이디
 * @returns 
 */
exports.deletePrintHistory = async (id) => {
    const query = `delete from print where id = ?`;
    return await pool(query, [id]);
}

