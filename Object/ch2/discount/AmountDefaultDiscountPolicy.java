package ch2.discount;

import ch2.Money;
import ch2.Screening;
import ch2.condition.DiscountCondition;

public class AmountDefaultDiscountPolicy extends DefaultDiscountPolicy {
    private Money discountAmount;

    public AmountDefaultDiscountPolicy(Money discountAmount, DiscountCondition... conditions) {
        super(conditions);
        this.discountAmount = discountAmount;
    }

    @Override
    protected  Money getDiscountAmount(Screening screening) {
        return discountAmount;
    }
}
