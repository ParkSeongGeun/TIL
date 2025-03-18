package ch2.condition;

import ch2.Screening;

public interface DiscountCondition {
    boolean isSatisfiedBy(Screening screening);
}
