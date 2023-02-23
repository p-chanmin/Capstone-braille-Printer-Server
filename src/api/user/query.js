const { pool } = require('../../data');

/**
 * 회원가입
 * @param {string} email    메일(아이디) 
 * @param {string} password 비밀번호
 * @param {string} name 이름
 * @returns 
 */
exports.register = async (email, password, name) => {
    const query = `INSERT INTO user
    (email, password, name)
    VALUES (?,?,?)`;
    return await pool(query, [email, password, name]);
}

/**
 * 로그인
 * @param {*} email 메일(아이디)
 * @param {*} password 비밀번호
 * @returns 
 */
exports.login = async (email, password) => {
    const query = `SELECT * FROM user WHERE
    email = ? AND password = ?`;
    let result = await pool(query, [email, password]);
    return (result.length < 0) ? null : result[0]
}

/**
 * 회원 탈퇴
 * @param {Int} userId 
 * @returns 
 */
exports.signOut = async (userId) => {
    const query = `DELETE FROM user WHERE id = ?;`;
    return await pool(query, [userId]);
}

exports.findUserbyEmail = async (email) => {
    const query = `SELECT * FROM user WHERE email = ?`;
    let result = await pool(query, [email]);
    return (result.length < 0) ? null : result[0]
}

exports.findUserbyId = async (userId) => {
    const query = `SELECT * FROM user WHERE id = ?`;
    let result = await pool(query, [userId]);
    return (result.length < 0) ? null : result[0]
}