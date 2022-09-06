import { checkStockCodeValidaty } from "../util/hkexAnalyticsHelper"

test("checkStockCodeValidity", () => {
    const validCode1 = "00001"
    const validCode2 = "00002"
    const invalidCode1 = "&1230"

    expect(checkStockCodeValidaty(validCode1)[0])
    expect(checkStockCodeValidaty(validCode2)[0])
    expect(!checkStockCodeValidaty(invalidCode1)[0])
})
