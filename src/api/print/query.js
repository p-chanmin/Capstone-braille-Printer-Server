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




exports.findUserbyEmail = async (email) => {
    const query = `SELECT * FROM user WHERE email = ?`;
    let result = await pool(query, [email]);
    return (result.length < 0) ? null : result[0]
}

