/** 사이트 메인 페이지 */
exports.home = (ctx, next) => {
    ctx.body = "Hello World";
}

/** 약관, 개인정보처리방침 등 정적 페이지 */
exports.page = async (ctx, next) => {
    let { page } = ctx.params;
    let pagename;
    switch (page) {
        case 'terms' :
            pagename = "이용약관";
            break;
        case 'policy':
            pagename = "개인정보 처리방침";
            break;
        default:
            pagename = "오류!";
            break;
    }
    await ctx.render('index', { pagename });
}