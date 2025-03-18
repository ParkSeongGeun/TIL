package ch2.discount;

import ch2.Money;
import ch2.Screening;

public interface DiscountPolicy {
    Money calculateDiscountAmount(Screening screening);
}
