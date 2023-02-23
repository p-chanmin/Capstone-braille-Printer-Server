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

